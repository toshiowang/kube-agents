"""Markdown constructs Google Chat renders badly, made readable.

Installed into the image at ``/opt/hermes/tools/gchat_markdown.py`` and called
from ``GoogleChatAdapter.format_message`` by ``apply_gchat_markdown.py``.

Upstream's ``format_message`` already converts the constructs Chat has a dialect
for — ``**bold**`` to ``*bold*``, ``## Heading`` to ``*Heading*``,
``[text](url)`` to ``<url|text>``. What it does not do is deal with the two
constructs Chat has no dialect for at all, and both of them are what a human
sees as "misaligned".

Measured against the deployed adapter on 2026-08-14, feeding it an ordinary
fleet-status reply::

    - Check the **prod-east** autoscaler
      - Review the node pool          <- two-space indent in, one space out

The final ``re.sub(r"  +", " ", text)`` in ``format_message`` exists to tidy the
double spaces left behind by stripping invisible codepoints, but it is not
anchored, so it eats *leading* whitespace too. Chat renders in a proportional
font, where a one-space indent is not distinguishable from none, so every nested
list arrives flat. :func:`collapse_interior_spaces` is the same tidy-up anchored
behind a non-space, which leaves indentation alone.

The second is tables. A Markdown pipe table reaches Chat verbatim and is drawn
in that same proportional font, so no column can ever line up — the wider the
values, the worse it reads. :func:`convert_tables` redraws them padded inside a
fenced block, which Chat renders monospaced, so the padding does what padding is
for.

Wide tables do not survive that trick: a monospace block wider than the phone
viewport is scrolled horizontally, which is worse than no table. Past
:data:`MAX_TABLE_WIDTH` the table is emitted as one labelled stanza per row
instead — taller, but every value stays on screen.

Why a fenced block rather than Chat's ``cardsV2`` grid: the agent posts text,
the card path (``card_spec_to_cards_v2``) is a separate entry point with its own
schema, and routing prose through it would change what every caller sends. This
converts text to text.

**Known limit.** ``_chunk_text`` splits at 4000 characters on the nearest
newline with no awareness of fences, so a converted table that straddles the
boundary arrives as an unclosed fence. That hazard predates this module — it is
true of any fenced block the agent writes today — and is not fixed here. It is
bounded by the same :data:`MAX_TABLE_WIDTH` fallback only incidentally; a very
long narrow table still reaches it.
"""

from __future__ import annotations

import re
from typing import Callable, List, Sequence

#: Widest monospace table worth drawing. Google Chat's message column is
#: narrower than a terminal and a phone narrower again; past this a fenced block
#: scrolls sideways, so the row-stanza fallback reads better.
MAX_TABLE_WIDTH = 76

#: A table separator: ``| --- | :--: |``. At least one dash, only the characters
#: a separator may contain, and at least one pipe so a lone ``---`` horizontal
#: rule is not mistaken for a one-column table.
_SEPARATOR_RE = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|[\s:|-]*$")

#: A horizontal rule: three or more ``-``, ``*`` or ``_`` alone on a line.
_HR_RE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")

#: What a horizontal rule becomes. Chat has no rule; box-drawing characters are
#: in its font and read as a divider rather than as stray punctuation.
_HR_TEXT = "─" * 24


def _split_row(line: str) -> List[str]:
    """Cells of one pipe-table row, outer pipes discarded."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _alignments(separator: str, columns: int) -> List[str]:
    """Per-column ``<``/``>``/``^`` from a separator row's colons."""
    marks = _split_row(separator)
    out: List[str] = []
    for index in range(columns):
        mark = marks[index] if index < len(marks) else ""
        left = mark.startswith(":")
        right = mark.endswith(":")
        out.append("^" if left and right else ">" if right else "<")
    return out


def _normalise(rows: Sequence[Sequence[str]], columns: int) -> List[List[str]]:
    """Pad every row to ``columns`` cells so zip/width maths cannot IndexError.

    A hand-written table with a short row is common and must not be a crash.
    """
    return [list(row[:columns]) + [""] * (columns - len(row)) for row in rows]


def _render_grid(header: List[str], body: List[List[str]], aligns: List[str]) -> str:
    """The padded monospace table, pipes kept so the columns read as columns."""
    columns = len(header)
    widths = [
        max(len(header[i]), *(len(row[i]) for row in body)) if body else len(header[i])
        for i in range(columns)
    ]

    def line(cells: Sequence[str]) -> str:
        out = []
        for index, cell in enumerate(cells):
            width = widths[index]
            align = aligns[index]
            if align == ">":
                out.append(cell.rjust(width))
            elif align == "^":
                out.append(cell.center(width))
            else:
                out.append(cell.ljust(width))
        return "| " + " | ".join(out) + " |"

    rule = "|" + "|".join("-" * (width + 2) for width in widths) + "|"
    return "\n".join([line(header), rule] + [line(row) for row in body])


def _render_stanzas(header: List[str], body: List[List[str]]) -> str:
    """One labelled stanza per row, for tables too wide to draw.

    The first column is the row's identity in every table an agent writes
    (cluster, workload, finding), so it becomes the bold label and the rest
    become ``Key: value`` lines under it.
    """
    blocks: List[str] = []
    for row in body:
        lines = [f"*{row[0]}*" if row[0] else "*—*"]
        for index in range(1, len(header)):
            if row[index]:
                lines.append(f"  {header[index]}: {row[index]}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _convert_one(block: List[str]) -> str:
    """Render one detected table, choosing grid or stanzas by width."""
    header = _split_row(block[0])
    columns = len(header)
    aligns = _alignments(block[1], columns)
    body = _normalise([_split_row(line) for line in block[2:]], columns)

    grid = _render_grid(header, body, aligns)
    if max(len(line) for line in grid.splitlines()) <= MAX_TABLE_WIDTH:
        return "```\n" + grid + "\n```"
    return _render_stanzas(header, body)


def convert_tables(text: str, protect: Callable[[str], str]) -> str:
    """Replace every Markdown pipe table with a Chat-readable rendering.

    ``protect`` is ``format_message``'s placeholder function. Every rendering
    goes through it because the rewrites that run afterwards would otherwise
    take the result apart: the ``**`` and ``_`` inside cell values would be
    re-interpreted, and the trailing space-collapse would strip out exactly the
    padding that makes the grid a grid.
    """
    if "|" not in text:
        return text

    lines = text.split("\n")
    out: List[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        is_table = (
            "|" in line
            and index + 1 < len(lines)
            and _SEPARATOR_RE.match(lines[index + 1])
            and "|" in lines[index + 1]
        )
        if not is_table:
            out.append(line)
            index += 1
            continue

        block = [line, lines[index + 1]]
        index += 2
        while index < len(lines) and "|" in lines[index] and lines[index].strip():
            block.append(lines[index])
            index += 1
        out.append(protect(_convert_one(block)))
    return "\n".join(out)


def convert_rules(text: str) -> str:
    """``---`` alone on a line becomes a divider Chat can actually draw.

    Runs after :func:`convert_tables`, which has already consumed the separator
    rows that would otherwise match.
    """
    return "\n".join(
        _HR_TEXT if _HR_RE.match(line) else line for line in text.split("\n")
    )


def collapse_interior_spaces(text: str) -> str:
    """Collapse runs of spaces *inside* a line, leaving indentation alone.

    Upstream's unanchored ``  +`` flattened nested lists; the lookbehind pins the
    match to a run that follows visible text, which is the only place the
    invisible-codepoint strip can leave a double space worth tidying.
    """
    return re.sub(r"(?<=\S)  +", " ", text)
