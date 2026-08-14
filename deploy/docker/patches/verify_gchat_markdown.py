#!/usr/bin/env python3
"""Build gate for the Google Chat Markdown rendering patch.

Run by ``deploy/docker/Dockerfile`` from ``/opt/hermes`` after
``apply_gchat_markdown.py``. The applier proves three anchors matched and that
the adapter still parses; it proves nothing about whether a message the agent
actually sends comes out readable, and every failure mode of this patch is
silent.

Three properties make a build-time gate non-optional here.

**The module is imported on every CLI invocation.** The plugin loader imports
``adapter.py`` at ``model_tools`` import time, and the file goes to some trouble
to defer its heavy google imports for exactly that reason. A patch that adds an
unresolvable module-level import turns every ``hermes`` command into a
traceback, and the applier's ``ast.parse`` cannot see an import that parses but
does not resolve. Check 1 imports the adapter the way the gateway does.

**The whole value is in the ordering.** ``convert_tables`` must run after the
inline-code guard, so a table inside a fenced block is left alone, and its
output must go through ``_ph``, or the space-collapse that runs later strips out
the padding that makes a grid a grid. Both are orderings a text match cannot
see, and both fail by producing a message that is merely ugly — which no
exception reports. Checks 2 and 3 drive the real ``format_message``.

**It must not break what already worked.** ``format_message`` had four
conversions before this patch touched it. Check 4 re-asserts every one, because
a regex inserted in the wrong place is far likelier to eat a heading than to
raise.

The four checks:

1. THE IMPORT RESOLVES, and ``format_message`` is still a classmethod on the
   real adapter class.
2. A TABLE, END TO END. Padded, fenced, and still padded after the collapse —
   the property that proves ``_ph`` was used rather than merely called.
3. INDENTATION SURVIVES. The exact regression measured against the deployed
   adapter on 2026-08-14: a two-space nested bullet arriving as one space.
4. NO REGRESSION. Headings, bold, links and code blocks all still convert, and
   a table written inside a code block is left alone.
"""

from __future__ import annotations

import sys

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    """Record a check, printing its verdict as the build log scrolls past."""
    if condition:
        print(f"  ok    {label}")
        return
    print(f"  FAIL  {label}")
    FAILURES.append(f"{label}{': ' + detail if detail else ''}")


def main() -> None:
    print("verify_gchat_markdown:")

    # --- 1. the import resolves ---------------------------------------------
    from plugins.platforms.google_chat.adapter import GoogleChatAdapter

    fmt = GoogleChatAdapter.format_message
    check("adapter imports with the patched module-level import", True)
    check("format_message is still callable", callable(fmt))

    # --- 2. a table, end to end ---------------------------------------------
    table_msg = (
        "Here are the clusters:\n"
        "\n"
        "| Cluster | Nodes | Status |\n"
        "| --- | --- | --- |\n"
        "| prod-east | 12 | Healthy |\n"
        "| staging | 3 | Degraded |\n"
    )
    out = fmt(table_msg)
    check("table is fenced for monospace", "```" in out, out)
    check(
        "columns are padded and the padding survived the space collapse",
        "| prod-east | 12    | Healthy  |" in out,
        out,
    )
    check(
        "header row is padded to the same width",
        "| Cluster   | Nodes | Status   |" in out,
        out,
    )
    check("prose around the table is kept", "Here are the clusters:" in out, out)

    # --- 3. indentation survives --------------------------------------------
    nested = "- Check the autoscaler\n  - Review the node pool\n    - Confirm quota\n"
    out = fmt(nested)
    check("two-space nested bullet keeps its indent", "\n  - Review" in out, out)
    check("four-space nested bullet keeps its indent", "\n    - Confirm" in out, out)

    # --- 4. nothing that worked before is broken ----------------------------
    check("heading still becomes bold", fmt("## Title") == "*Title*", fmt("## Title"))
    check("bold still converts", fmt("**hi**") == "*hi*", fmt("**hi**"))
    check(
        "link still converts",
        fmt("[docs](https://example.com)") == "<https://example.com|docs>",
        fmt("[docs](https://example.com)"),
    )
    fenced = "```\n| a | b |\n| --- | --- |\n| 1 | 2 |\n```"
    check(
        "a table inside a code block is left alone",
        fmt(fenced) == fenced,
        fmt(fenced),
    )
    inline = "use `| a | b |` here"
    check("inline code is left alone", fmt(inline) == inline, fmt(inline))
    check(
        "interior double space is still collapsed",
        fmt("a  b") == "a b",
        fmt("a  b"),
    )
    check("empty input still passes through", fmt("") == "", repr(fmt("")))

    print()
    if FAILURES:
        print(f"verify_gchat_markdown: {len(FAILURES)} FAILED")
        for failure in FAILURES:
            print(f"  - {failure}")
        raise SystemExit(1)
    print("verify_gchat_markdown: all checks passed")


if __name__ == "__main__":
    sys.exit(main())
