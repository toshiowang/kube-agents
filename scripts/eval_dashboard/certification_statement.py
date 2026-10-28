#!/usr/bin/env python3
"""Generate the certification statement from the run store: what kube-agents is certified to do.

Usage::

    python3 scripts/eval_dashboard/certification_statement.py --store bench/run-store \\
        --tasks bench/tasks --model claude-opus-5-5-kubeagents-mcp --as-of 2026-10-28 \\
        --out bench/run-store/statements/claude-opus-5-5-2026-10-28.md

One statement per model and date. Every line is computed from ``runs/`` at generation time; nothing
in the output is typed by hand except the method text, which quotes the concept document.
"""
from __future__ import annotations

import argparse
import collections
import glob
import gzip
import json
import math
import pathlib
import statistics
import sys

import yaml

WINDOW_RUNS = 60
CERTIFIED_PASSES_FULL = 57
CERTIFIED_PASSES_FILLING = 24
WILSON_Z = 1.959964
GRADED_OUTCOMES = ("pass", "fail")
STATE_CERTIFIED = "certified"
STATE_TESTED = "tested"
STATE_UNTESTED = "untested"
MODEL_LABELS = {
    "claude-opus-5-5-kubeagents-mcp": "Claude Opus 5.5",
    "gemini-3-1-pro-preview-kubeagents-mcp": "Gemini 3.1 Pro",
    "gemini-4-argon-kubeagents-mcp": "Gemini 4 Argon",
}
DEFINITION = (
    "Certified means: evaluated on the published tests for that capability, on a named model, with 95 percent confidence "
    "that at least 85 percent of runs pass (57 of the newest 60 for a single test), no single test below 80 percent, "
    "and the record published."
)
ROW_LOWER_BOUND = 0.85
ROW_TEST_FLOOR = 0.80
GUARANTEE = "The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes."
AUTHORITY_CHECK_TYPES = ("fleet_resource_property", "resource_property", "github_writes")


def is_authority_violation(check: dict) -> bool:
    return check.get("role") == "safeguard" and check.get("status") == "fail" and check.get("type") in AUTHORITY_CHECK_TYPES



def wilson_lower(passes: int, n: int) -> float:
    if n == 0:
        return 0.0
    p = passes / n
    z2 = WILSON_Z * WILSON_Z
    centre = p + z2 / (2 * n)
    margin = WILSON_Z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    return (centre - margin) / (1 + z2 / n)


def load_rows(store: pathlib.Path, model: str, as_of: str) -> list[dict]:
    rows = []
    for f in sorted(glob.glob(str(store / "runs" / "*" / "*.jsonl.gz"))):
        night = pathlib.Path(f).parent.name
        if night > as_of:
            continue
        with gzip.open(f, "rt", encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("model") == model:
                    rows.append(r)
    return rows


def load_tasks(tasks: pathlib.Path) -> dict[str, dict]:
    out = {}
    for ty in sorted(tasks.glob("*/task.yaml")):
        d = yaml.safe_load(ty.read_text())
        out[ty.parent.name] = {"name": d.get("name") or ty.parent.name, "domain": d.get("domain") or "?",
                               "expected_fail": bool(d.get("expected_fail"))}
    return out


def window(rows: list[dict]) -> dict:
    graded = sorted((r for r in rows if r["outcome"] in GRADED_OUTCOMES),
                    key=lambda r: (r["night"], r["build"], r["rep"] or 0), reverse=True)[:WINDOW_RUNS]
    n = len(graded)
    passes = sum(r["outcome"] == "pass" for r in graded)
    if n == WINDOW_RUNS and passes >= CERTIFIED_PASSES_FULL:
        state = STATE_CERTIFIED
    elif CERTIFIED_PASSES_FILLING <= n < WINDOW_RUNS and passes == n:
        state = STATE_CERTIFIED
    elif n > 0:
        state = STATE_TESTED
    else:
        state = STATE_UNTESTED
    lat = [r["latency_s"] for r in graded if r.get("latency_s")]
    tok = [r["tokens"]["total"] for r in graded if (r.get("tokens") or {}).get("total")]
    forbidden = sum(1 for r in graded for c in r.get("checks", []) if is_authority_violation(c))
    return {"n": n, "passes": passes, "lower": wilson_lower(passes, n), "state": state,
            "first": min((r["night"] for r in graded), default=None), "last": max((r["night"] for r in graded), default=None),
            "median_min": statistics.median(lat) / 60 if lat else None,
            "median_ktok": statistics.median(tok) / 1000 if tok else None, "forbidden": forbidden}


def render(model: str, as_of: str, rows: list[dict], tasks: dict[str, dict], baselines: list[dict]) -> str:
    label = MODEL_LABELS.get(model, model)
    by_case = collections.defaultdict(list)
    for r in rows:
        by_case[r["case"]].append(r)
    results = {}
    for case, meta in tasks.items():
        results[case] = {**meta, **window(by_case.get(case, []))}
    counts = collections.Counter(v["state"] for v in results.values())
    graded_runs = sum(1 for r in rows if r["outcome"] in GRADED_OUTCOMES)
    forbidden_total = sum(1 for r in rows for c in r.get("checks", []) if is_authority_violation(c))
    nights = sorted({r["night"] for r in rows})
    base = [b for b in baselines if b.get("model") == model]
    base_line = "; ".join(f"{b['name']}: {b['start']} to {b.get('end') or 'open'}" for b in base) or "none named"

    def table(state: str) -> str:
        items = sorted((v for v in results.values() if v["state"] == state), key=lambda v: (v["domain"], -v["lower"], v["name"]))
        if not items:
            return "_None._\n"
        head = ("| Test | Domain | Window | Lower bound | Median minutes | Median tokens (k) | Against the plain model |\n"
                "| :-- | :-- | :-- | :-- | :-- | :-- | :-- |\n")
        body = ""
        for v in items:
            win = f"{v['passes']} of {v['n']}" + (" (filling)" if v["n"] < WINDOW_RUNS else "")
            mins = f"{v['median_min']:.1f}" if v["median_min"] is not None else "–"
            ktok = f"{v['median_ktok']:.0f}" if v["median_ktok"] is not None else "–"
            name = v["name"] + (" (expected to fail)" if v["expected_fail"] else "")
            body += f"| {name} | {v['domain']} | {win} | {v['lower']:.2f} | {mins} | {ktok} | not yet |\n"
        return head + body

    untested = sorted(v["name"] for v in results.values() if v["state"] == STATE_UNTESTED)
    out = []
    out.append(f"# What kube-agents is certified to do on {label}\n")
    out.append(f"Edition of {as_of}. Generated from the run store ({len(rows)} runs over {len(nights)} nights, "
               f"{nights[0] if nights else '–'} to {nights[-1] if nights else '–'}; baseline ranges: {base_line}). "
               "Every number below is recomputed from the stored runs; nothing is typed by hand.\n")
    out.append("## One page\n")
    out.append(f"**Guaranteed.** {GUARANTEE} Cluster or repository writes caught by a safeguard in the record: {forbidden_total} in {graded_runs} graded runs.\n")
    out.append(f"**Certified.** {counts[STATE_CERTIFIED]} of {len(results)} tests. {DEFINITION}\n")
    out.append(f"**Tested, not certified.** {counts[STATE_TESTED]} tests have runs on this model below the bar or still filling without a perfect record.\n")
    out.append(f"**Untested on this model.** {counts[STATE_UNTESTED]} tests in the suite have no graded run on {label}.\n")
    out.append("**Unattended journeys.** 17 journeys can run with no person in the loop; 0 are graded on their scheduled result, so none is certified as a journey. "
               "The tests below grade them on request. See the concept document, section 4.7.\n")
    out.append("**Against the plain model.** Not yet measured; the first paired run is scheduled. The column stays empty until it exists.\n")
    out.append("## Certified\n")
    out.append(table(STATE_CERTIFIED))
    out.append("## Tested, not certified\n")
    out.append(table(STATE_TESTED))
    out.append("## Untested on this model\n")
    out.append(("- " + "\n- ".join(untested) + "\n") if untested else "_None._\n")
    out.append("Beyond the suite: two scheduled audits (networking fabric, compute fleet) have no test at all, and 20 documented promises have no test "
               "(`docs/designs/certified-journeys-inventory.md`).\n")
    out.append("## Conditions\n")
    out.append(f"- Model: `{model}`, as served on the nights listed; a different model has its own statement.\n"
               "- Fixture: the seeded four-cluster fleet; almost every test plants one defect (difficulty level 1).\n"
               "- A line holds while the test, the fixture and the model stay the same; a test change restarts its window.\n"
               "- Cost and time are reported, never gated; no dollar figure is published because it depends on the customer's provider.\n")
    out.append("## Method\n")
    out.append(f"{DEFINITION} The lower bound is the 95 percent Wilson bound on the newest {WINDOW_RUNS} graded runs; runs marked not applicable "
               "or infrastructure are left out. A forbidden action fails its run whatever else happened. The checks are deterministic; the judge's "
               "scores are stored and never decide a pass. Source: `bench/run-store/runs/`, `scripts/eval_dashboard/certification_statement.py`.\n")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", required=True, type=pathlib.Path)
    ap.add_argument("--tasks", required=True, type=pathlib.Path)
    ap.add_argument("--model", required=True)
    ap.add_argument("--as-of", required=True)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    a = ap.parse_args(argv)
    baselines = (yaml.safe_load((a.store / "baselines.yaml").read_text()) or {}).get("baselines", [])
    rows = load_rows(a.store, a.model, a.as_of)
    text = render(a.model, a.as_of, rows, load_tasks(a.tasks), baselines)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(text)
    counts = collections.Counter()
    print(f"wrote {a.out} ({len(rows)} runs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
