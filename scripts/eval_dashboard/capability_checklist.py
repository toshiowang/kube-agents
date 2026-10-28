#!/usr/bin/env python3
"""The checklist: what kube-agents can and cannot do on one model, from the run store.

Usage::

    python3 scripts/eval_dashboard/capability_checklist.py --store bench/run-store --tasks bench/tasks \\
        --model claude-opus-5-5-kubeagents-mcp --as-of 2026-10-28 --out bench/run-store/statements/checklist-claude-2026-10-28.md

Rows come from ``capabilities.yaml``; every status is computed from ``runs/``.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from certification_statement import (CERTIFIED_PASSES_FILLING, DEFINITION, GUARANTEE, MODEL_LABELS,  # noqa: E402
                                     STATE_CERTIFIED, is_authority_violation, load_rows, load_tasks, window)

CAN = "✅ Can"
FILLING = "🕒 Filling"
MOSTLY = "🟡 Mostly"
PARTLY = "🟠 Partly"
NOT_YET = "❌ Not yet"
NO_TEST = "⬜ No test"
PARTLY_MIN_RATE = 0.5
MOSTLY_MIN_RATE = 0.8


def status(windows: list[dict]) -> tuple[str, str, dict]:
    """(label, one-line evidence, numbers) for one checklist row."""
    with_runs = [w for w in windows if w["n"] > 0]
    numbers = {"tests": len(windows), "tests_with_runs": len(with_runs), "certified": 0, "passes": 0, "n": 0, "min_window": 0}
    if not with_runs:
        return NO_TEST, ("no graded run on this model" if windows else "no test exists"), numbers
    certified = sum(w["state"] == STATE_CERTIFIED for w in with_runs)
    n = sum(w["n"] for w in with_runs)
    passes = sum(w["passes"] for w in with_runs)
    numbers.update(certified=certified, passes=passes, n=n, min_window=min(w["n"] for w in with_runs))
    rate = passes / n
    detail = f"{certified} of {len(with_runs)} tests at the bar; {passes} of {n} runs pass"
    if certified == len(with_runs):
        return CAN, detail, numbers
    if passes == n:
        return FILLING, f"no failure yet; the smallest window has {numbers['min_window']} of {CERTIFIED_PASSES_FILLING} runs", numbers
    if rate >= MOSTLY_MIN_RATE:
        return MOSTLY, detail, numbers
    if certified or rate >= PARTLY_MIN_RATE:
        return PARTLY, detail, numbers
    return NOT_YET, detail, numbers


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", required=True, type=pathlib.Path)
    ap.add_argument("--tasks", required=True, type=pathlib.Path)
    ap.add_argument("--model", required=True)
    ap.add_argument("--as-of", required=True)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--out-json", type=pathlib.Path, help="also write the rows and numbers as JSON for the HTML renderer")
    a = ap.parse_args(argv)
    label = MODEL_LABELS.get(a.model, a.model)
    rows = load_rows(a.store, a.model, a.as_of)
    tasks = load_tasks(a.tasks)
    by_case: dict[str, list[dict]] = {}
    for r in rows:
        by_case.setdefault(r["case"], []).append(r)
    spec = yaml.safe_load((a.store / "capabilities.yaml").read_text())
    nights = sorted({r["night"] for r in rows})
    graded = [r for r in rows if r["outcome"] in ("pass", "fail")]
    authority_fails = sum(1 for r in graded for c in r.get("checks", []) if is_authority_violation(c))
    other_safeguard_fails = sum(1 for r in graded for c in r.get("checks", [])
                                if c.get("role") == "safeguard" and c.get("status") == "fail" and not is_authority_violation(c))
    out = [f"# What kube-agents can and cannot do today, on {label}\n",
           f"Edition of {a.as_of}, computed from {len(graded)} graded runs over {len(nights)} nights "
           f"({nights[0] if nights else '–'} to {nights[-1] if nights else '–'}). Legend: {CAN} = every evidence test is at the bar; "
           f"{FILLING} = no failure yet, window still short of 24 runs; {MOSTLY} = at least 80 percent of runs pass, below the bar; {PARTLY} = between 50 and 79 percent of runs pass; {NOT_YET} = fewer than half the runs pass; {NO_TEST} = no test, or none run on this model.\n",
           f"**Guaranteed.** {GUARANTEE} Cluster or repository writes caught by a safeguard in this record: {authority_fails}. "
           f"Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): {other_safeguard_fails}.\n",
           f"**What certified means.** {DEFINITION}\n"]
    totals = {CAN: 0, FILLING: 0, MOSTLY: 0, PARTLY: 0, NOT_YET: 0, NO_TEST: 0}
    doc = {"model": a.model, "label": label, "as_of": a.as_of, "nights": nights, "graded_runs": len(graded),
           "authority_fails": authority_fails, "other_safeguard_fails": other_safeguard_fails,
           "definition": DEFINITION, "guarantee": GUARANTEE, "groups": []}
    for g in spec["groups"]:
        out.append(f"## {g['name']}\n")
        doc_group = {"name": g["name"], "scheduled": bool(g.get("scheduled")), "rows": []}
        doc["groups"].append(doc_group)
        sched = g.get("scheduled")
        head = "| Capability | Status | Evidence | Graded on its schedule? | Note |\n| :-- | :-- | :-- | :-- | :-- |\n" if sched \
            else "| Capability | Status | Evidence | Note |\n| :-- | :-- | :-- | :-- |\n"
        body = ""
        for row in g["rows"]:
            ids = sorted({t for pat in row.get("tests", []) for t in tasks if fnmatch.fnmatch(t, pat)})
            windows = [window(by_case.get(t, [])) for t in ids]
            st, detail, numbers = status(windows)
            totals[st] += 1
            note = row.get("note", "")
            doc_group["rows"].append({"capability": row["capability"], "status": st, "detail": detail, "note": note, "tests": ids, **numbers})
            if sched:
                body += f"| {row['capability']} | {st} | {detail} | ❌ not yet | {note} |\n"
            else:
                body += f"| {row['capability']} | {st} | {detail} | {note} |\n"
        out.append(head + body)
    out.insert(4, "| " + " | ".join(totals) + " |\n| :-- | :-- | :-- | :-- | :-- | :-- |\n| " + " | ".join(str(v) for v in totals.values()) + " |\n")
    out.append("## Not in this checklist\n")
    out.append("Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; "
               "any comparison against a plain model, which the first paired run will add as a column.\n")
    out.append("## Method\n")
    out.append("Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, "
               "95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.\n")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(out))
    if a.out_json:
        doc["totals"] = totals
        a.out_json.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print(f"wrote {a.out}: " + ", ".join(f"{k} {v}" for k, v in totals.items()) + f"; authority fails {authority_fails}, other safeguard fails {other_safeguard_fails}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
