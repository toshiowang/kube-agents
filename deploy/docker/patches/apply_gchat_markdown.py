#!/usr/bin/env python3
"""Wire tools/gchat_markdown.py into the Google Chat adapter.

Run by ``deploy/docker/Dockerfile`` against ``/opt/hermes``. Three anchored
replacements in ``plugins/platforms/google_chat/adapter.py``, all inside
``GoogleChatAdapter.format_message`` except the import. Every anchor must be
found exactly once and the file must still parse, or the build fails loudly
rather than shipping an image whose chat output is not the one this patch
describes.

Why each edit is needed is documented in the module docstring of
``deploy/docker/patches/gchat_markdown.py``. Usage::

    python3 apply_gchat_markdown.py [HERMES_ROOT]   # default /opt/hermes
"""

from __future__ import annotations

import sys
from pathlib import Path

import patchlib

ADAPTER = "plugins/platforms/google_chat/adapter.py"

# --- the import -------------------------------------------------------------
# Anchored on the typing line rather than added at the top of the file: this
# module is imported by the plugin loader at ``model_tools`` import time, so
# every ``hermes`` CLI invocation pays for whatever lands here. gchat_markdown
# imports only ``re`` and ``typing``, which is why a module-level import is
# acceptable at all — see the deferred-google-imports comment just below it.
IMPORT_ANCHOR = "from typing import Any, Callable, Dict, List, Optional, Tuple"

IMPORT_PATCHED = (
    IMPORT_ANCHOR + "\n"
    "\n"
    "# kube-agents patch: see tools/gchat_markdown.py. Stdlib-only, so it does\n"
    "# not reintroduce the import cost the deferred google imports below avoid.\n"
    "from tools import gchat_markdown as _gchat_markdown"
)

# --- tables -----------------------------------------------------------------
# Inserted after the inline-code guard so a pipe table written *inside* a code
# block is already a placeholder and is left alone. The conversion protects its
# own output through the same ``_ph``, because the rewrites below would
# otherwise re-interpret cell contents and the space-collapse would strip the
# padding that makes the grid align.
TABLE_ANCHOR = '        text = re.sub(r"(`[^`]+`)", lambda m: _ph(m.group(0)), text)\n'

TABLE_PATCHED = (
    TABLE_ANCHOR + "\n"
    "        # kube-agents patch: Markdown pipe tables reach Chat verbatim and are\n"
    "        # drawn in a proportional font, so no column lines up. Redraw them\n"
    "        # padded inside a fence. See tools/gchat_markdown.py.\n"
    "        text = _gchat_markdown.convert_tables(text, _ph)\n"
)

# --- rules, and the collapse that ate list indentation ----------------------
# The unanchored ``  +`` was tidying the double spaces left by the invisible
# codepoint strip, but it matched leading whitespace too, so every nested list
# arrived flat. Measured 2026-08-14 against the deployed adapter: a two-space
# indent came out as one space, which a proportional font cannot show.
COLLAPSE_ANCHOR = (
    "        # Collapse double spaces left over from stripped chars.\n"
    '        text = re.sub(r"  +", " ", text)\n'
)

COLLAPSE_PATCHED = (
    "        # kube-agents patch: `---` becomes a divider Chat can draw. Runs\n"
    "        # after convert_tables, which has consumed separator rows already.\n"
    "        text = _gchat_markdown.convert_rules(text)\n"
    "\n"
    "        # Collapse double spaces left over from stripped chars.\n"
    "        # kube-agents patch: anchored behind a non-space so this no longer\n"
    "        # eats the leading indentation of a nested list.\n"
    "        text = _gchat_markdown.collapse_interior_spaces(text)\n"
)

PATCHES = (
    (IMPORT_ANCHOR, IMPORT_PATCHED, 1),
    (TABLE_ANCHOR, TABLE_PATCHED, 1),
    (COLLAPSE_ANCHOR, COLLAPSE_PATCHED, 1),
)


def apply(root: Path) -> None:
    """Apply every edit under ``root``, or raise SystemExit with the reason."""
    patch = patchlib.Patch(root, ADAPTER, prefix="gchat_markdown")
    for anchor, replacement, expected in PATCHES:
        patch.substitute(anchor, replacement, expected=expected)
    patch.commit(f"{len(PATCHES)} anchors")


if __name__ == "__main__":
    apply(Path(sys.argv[1] if len(sys.argv) > 1 else "/opt/hermes"))
