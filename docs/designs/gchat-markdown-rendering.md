# Google Chat Markdown Rendering

The agent writes Markdown. Google Chat renders a small, different dialect of it.
This document records which constructs fall through that gap, what the image
does about it, and what is deliberately left unfixed.

## 1. Why

Chat messages from the Platform Agent read as misaligned. The complaint is
vague; the cause is not. Feeding the deployed adapter an ordinary fleet-status
reply on 2026-08-14 reproduced exactly two defects, and between them they
account for what a human sees.

`GoogleChatAdapter.format_message` in
`plugins/platforms/google_chat/adapter.py` already handles every construct Chat
has a dialect for: `**bold**` becomes `*bold*`, `## Heading` becomes `*Heading*`,
`[text](url)` becomes `<url|text>`, and fenced and inline code are protected
from all of it by placeholder substitution. That part works. The gap is the
constructs Chat has no dialect for at all.

**Nested lists arrive flat.** The last thing `format_message` does is

```python
text = re.sub(r"  +", " ", text)
```

which exists to tidy the double spaces left behind by stripping invisible
codepoints. It is not anchored, so it matches _leading_ whitespace too. A
two-space indent leaves as a one-space indent, and Chat renders in a
proportional font where one space is not distinguishable from none:

```
- Check the prod-east autoscaler
  - Review the node pool          <- two spaces in, one space out
```

**Pipe tables are drawn in a proportional font.** A Markdown table reaches Chat
verbatim. Chat has no table support, so it lays the pipes out in the body font,
where no column can line up — and the more the cell widths differ, the worse it
reads. This is the construct the agent reaches for most in a fleet report.

## 2. The target model

One stdlib-only module, `tools/gchat_markdown.py`, called from three points
inside the existing `format_message`. No new entry point, no change to what any
caller sends, no change to the adapter's structure.

| Construct           | Before               | After                                   |
| ------------------- | -------------------- | --------------------------------------- |
| Nested list         | indent collapsed     | indent preserved                        |
| Pipe table (narrow) | raw pipes, unaligned | padded grid inside a fence (monospaced) |
| Pipe table (wide)   | raw pipes, unaligned | one labelled stanza per row             |
| `---`               | literal dashes       | a box-drawing divider                   |
| Everything else     | —                    | unchanged                               |

### Where the calls go, and why it matters

Ordering is the design. Both requirements are invisible to a text match and both
fail silently, which is why they are asserted at build time rather than trusted.

1. **`convert_tables` runs after the inline-code guard.** By that point a table
   written inside a fenced or inline code block is already a placeholder, so it
   is left alone — which is what a user who deliberately pasted a table into a
   code block asked for.
2. **`convert_tables` routes its output back through the adapter's own `_ph`.**
   Without that, the rewrites that follow take the result apart: `**` and `_`
   inside cell values get re-interpreted as emphasis, and the trailing
   space-collapse strips out the very padding that makes the grid a grid. The
   padded table would arrive less aligned than the raw one.
3. **`convert_rules` runs before the collapse and after `convert_tables`**, which
   has already consumed the separator rows a rule regex would otherwise match.

## 3. Decisions

### 3.1 A fenced block, not a `cardsV2` grid

Chat can draw a real grid through `cardsV2`, and it would look better than
monospace. It is rejected because the agent posts text. The card path
(`card_spec_to_cards_v2`) is a separate entry point with its own schema, and
routing prose through it would change what every caller sends and what every
non-card consumer receives. This conversion is text to text, which keeps the
blast radius at the one function.

### 3.2 Wide tables degrade to stanzas rather than scrolling

A monospace block wider than the viewport is scrolled horizontally, and on a
phone that is worse than no table — values leave the screen entirely. Past
`MAX_TABLE_WIDTH` (76 characters) the table is re-emitted as one stanza per row:
the first column bolded as the row's label, the remaining columns as indented
`Key: value` lines. Taller, but nothing goes off-screen.

76 is chosen against Chat's message column rather than a terminal's 80, and the
threshold is measured on the rendered grid, not the source, so a table only
falls back when padding actually pushed it over.

### 3.3 The collapse is anchored, not deleted

The double-space tidy-up has a real job: the invisible-codepoint strip just above
it leaves gaps behind. Deleting it would trade one cosmetic defect for another.
`(?<=\S)  +` keeps the tidy-up exactly where it was useful — a run of spaces
following visible text — and takes it out of the one place it was harmful.

### 3.4 The patch is verified behaviourally at build time

`apply_gchat_markdown.py` proves three anchors matched exactly once each and that
the file still parses. That is necessary and nowhere near sufficient: every
failure mode here is silent. A module-level import that parses but does not
resolve turns every `hermes` CLI invocation into a traceback, and `ast.parse`
cannot see it. A `convert_tables` call inserted one line too early, or handed
`str` instead of `_ph`, produces a message that is merely ugly, and nothing
raises. `verify_gchat_markdown.py` therefore imports the adapter the way the
gateway does and drives the real patched `format_message`, asserting on the
output — including that the column padding is still present _after_ the collapse,
which is the property that proves `_ph` was actually used.

## 4. Work breakdown

1. `tools/gchat_markdown.py` — the conversions, stdlib only.
2. `apply_gchat_markdown.py` — three anchored substitutions via `patchlib`.
3. `verify_gchat_markdown.py` — the behavioural build gate.
4. `test_gchat_markdown.py` — unit tests over the module in isolation.
5. One `COPY` + one `RUN` in the Dockerfile.

## 5. Files touched

| File                                             | Change                                          |
| ------------------------------------------------ | ----------------------------------------------- |
| `deploy/docker/patches/gchat_markdown.py`        | New. The conversions.                           |
| `deploy/docker/patches/apply_gchat_markdown.py`  | New. Three anchors on the adapter.              |
| `deploy/docker/patches/verify_gchat_markdown.py` | New. Build gate over the real function.         |
| `deploy/docker/patches/test_gchat_markdown.py`   | New. Unit tests.                                |
| `deploy/docker/Dockerfile`                       | One `COPY`, one `RUN`, after the latency block. |
| `docs/README.md`                                 | One row for this document.                      |

No agent configuration, persona, or skill changes: the agent keeps writing
ordinary Markdown, and the adapter stops mangling it. Steering the model to write
Chat-flavoured text instead was considered and dropped — it would need to hold
across every skill and every profile, and it would still be wrong for the Slack
adapter, which has its own dialect and its own patch.

### Layer budget

`credential-proxy` builds `FROM platform` and has hit Docker's overlay2
128-layer ceiling once before (build f9f1747c, 2026-08-07). The deployed image
measures 116 layers against the 120-layer budget in
`scripts/check_image_layers.py`, so the usual three-layer patch block (module
`COPY`, staging `COPY`, `RUN`) would leave one layer of headroom. This ships as
one `COPY` plus one `RUN` — the module is `cp`'d into `/opt/hermes/tools/` by the
`RUN` rather than buying a `COPY` of its own — for 118. Same applier, same greps,
same behavioural verify; only the layer count differs.

## 6. Testing

- **Unit** (`make test-python`): the conversions in isolation, including the
  measured regression pinned as its own case — a two-space indent must survive
  `collapse_interior_spaces`.
- **Build gate** (`verify_gchat_markdown.py`): the real patched `format_message`,
  covering the import resolving, a table end to end with its padding intact after
  the collapse, indentation surviving, and no regression on headings, bold,
  links, fenced blocks, inline code or empty input.
- **Live**: post a message containing a table and a nested list through the
  deployed agent and read it in Chat.

## 7. Accepted risks

**A converted table can straddle a chunk boundary.** `_chunk_text` splits at
4,000 characters on the nearest newline with no awareness of fences, so a fenced
block spanning the split arrives with an unclosed fence. This hazard predates
this change — it is already true of any fenced block the agent writes — and is
not fixed here. It is not addressed because fixing it means teaching the chunker
about fences, which is a change to the splitting path that every message takes,
not just the ones with tables. What this change does is make fenced blocks more
common, so the pre-existing bug gets more chances to fire. The
`MAX_TABLE_WIDTH` fallback bounds it only incidentally: a long narrow table still
reaches the limit.

**Cell contents are not re-escaped.** A cell containing a pipe character will
split into two cells. Markdown's own escape (`\|`) is not honoured. This is the
same behaviour the raw table had, so nothing regresses, but the padded grid makes
it look deliberate rather than broken.

**Alignment markers are honoured, but Chat's font is not guaranteed.** The grid
depends on Chat rendering a fenced block in a fixed-width font. That is current
behaviour on every Chat client, and it is not a documented API contract.
