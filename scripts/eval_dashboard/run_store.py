#!/usr/bin/env python3
"""Build the per-run store from cached nightly artifacts: one JSON line per run.

Usage::

    python3 scripts/eval_dashboard/run_store.py build --cache DIR --out bench/run-store/runs

Reads every build under ``<cache>/<job>/<build>/`` (the layout ``skill_use.py fetch`` writes:
``started.json`` plus ``artifacts/case-*.json``, ``artifacts/results_<case>_rep<n>.json`` and the
run directories) and writes ``<out>/<night>/<job>.jsonl.gz``, one object per repetition, plus
``<out>/index.json`` with the counts per night and job. Append-only by construction: a night's
file is rewritten only from the same immutable artifacts, and a later re-grade adds rows whose
``grader`` is not ``as-recorded`` instead of changing these.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import gzip
import json
import pathlib
import sys

GRADER_AS_RECORDED = "as-recorded"
REASON_MAX_CHARS = 200
TOKEN_FIELDS = ("input", "cached", "cache_write", "reasoning", "output", "total")
JUDGED_FIELDS = ("OutcomeValidity", "ToolInvocation", "OutcomeScore")
SKILL_VIEW_TOOL = "skill_view"
INDEX_FILE = "index.json"
STARTED_FILE = "started.json"
MANIFEST_FILE = "manifest.json"


def _night(started: dict) -> str:
    return dt.datetime.fromtimestamp(int(started["timestamp"]), dt.timezone.utc).strftime("%Y-%m-%d")


def _tokens(results: dict) -> tuple[dict, dict]:
    raw = results.get("tokens") or {}
    top = {k: raw.get(k) for k in TOKEN_FIELDS}
    source = top
    workers = raw.get("workers") or {}
    if top.get("total") is None and workers.get("total") is not None:
        source = {k: workers.get(k) for k in TOKEN_FIELDS}
    by_agent = {a: (v or {}).get("total") for a, v in (workers.get("by_agent") or {}).items()}
    return source, by_agent


def _skills_opened(results: dict) -> list[str]:
    names: list[str] = []
    for step in results.get("trajectory") or []:
        if step.get("name") == SKILL_VIEW_TOOL:
            name = (step.get("args") or {}).get("name")
            if name and name not in names:
                names.append(name)
    return names


def _checks(results: dict) -> tuple[list[dict], dict]:
    rows, counts = [], collections.Counter()
    for v in results.get("verification_report") or []:
        role, status = v.get("role"), v.get("status")
        rows.append({
            "name": v.get("name"), "role": role, "status": status, "success": v.get("success"),
            "severity": v.get("severity"), "reason": (v.get("reason") or "")[:REASON_MAX_CHARS],
        })
        counts[f"{role}_{status}"] += 1
    return rows, dict(counts)


def _results_for(art: pathlib.Path, case: str, rep: dict) -> tuple[dict | None, str | None]:
    for idx in (rep.get("index"), (rep.get("index") or 0) + 1):
        p = art / f"results_{case}_rep{idx}.json"
        if p.exists():
            data = json.loads(p.read_text())
            return (data[0] if isinstance(data, list) and data else data), p.name
    return None, None


def _model_id(art: pathlib.Path, run_dir: str | None) -> str | None:
    if not run_dir:
        return None
    p = art / pathlib.Path(run_dir).name / MANIFEST_FILE
    if p.exists():
        try:
            return json.loads(p.read_text()).get("model")
        except json.JSONDecodeError:
            return None
    return None


def build_rows(build_dir: pathlib.Path, job: str) -> list[dict]:
    started = json.loads((build_dir / STARTED_FILE).read_text())
    night, commit = _night(started), started.get("repo-commit")
    art = build_dir / "artifacts"
    rows: list[dict] = []
    for case_file in sorted(art.glob("case-*.json")) if art.exists() else []:
        case = json.loads(case_file.read_text())
        key = case.get("version_key") or {}
        for rep in case.get("reps") or []:
            results, results_file = _results_for(art, case["case"], rep)
            tokens, by_agent = _tokens(results or {})
            checks, check_counts = _checks(results or {})
            judged = rep.get("judged") or {}
            rows.append({
                "night": night, "job": job, "build": build_dir.name, "commit": commit,
                "case": case["case"], "domain": case.get("domain"), "rep": rep.get("index"),
                "run_dir": rep.get("run_dir"), "results_file": results_file,
                "expected_fail": case.get("expected_fail"), "admitted": case.get("admitted"),
                "record_verdict": case.get("record_verdict"),
                "outcome": rep.get("outcome"), "reason": (rep.get("reason") or "")[:REASON_MAX_CHARS],
                "rung": rep.get("rung"),
                "model": key.get("setup_id"), "model_id": _model_id(art, rep.get("run_dir")),
                "scoring_version": key.get("scoring_version"), "judge_model": key.get("judge_model"),
                "fleet": key.get("fleet"), "verifiers": key.get("verifiers"), "mode": key.get("mode"),
                "latency_s": rep.get("latency"), "turn1_s": rep.get("turn1_s"),
                "tokens": tokens, "tokens_by_agent": by_agent,
                "judged": {k: judged.get(k) for k in JUDGED_FIELDS},
                "correctness": rep.get("correctness"), "coverage": rep.get("coverage"),
                "catastrophic": rep.get("catastrophic"),
                "not_applicable_checks": rep.get("not_applicable_checks") or [],
                "checks": checks, "check_counts": check_counts,
                "tools": sorted(set((results or {}).get("tools") or [])),
                "tool_calls": len((results or {}).get("trajectory") or []),
                "skills_opened": _skills_opened(results or {}),
                "grader": GRADER_AS_RECORDED,
            })
    return rows


def build(cache: pathlib.Path, out: pathlib.Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    per_night: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    builds = []
    for job_dir in sorted(p for p in cache.iterdir() if p.is_dir()):
        for build_dir in sorted(p for p in job_dir.iterdir() if p.is_dir()):
            if not (build_dir / STARTED_FILE).exists():
                continue
            rows = build_rows(build_dir, job_dir.name)
            if not rows:
                continue
            per_night[(rows[0]["night"], job_dir.name)].extend(rows)
            builds.append({"night": rows[0]["night"], "job": job_dir.name, "build": build_dir.name,
                           "commit": rows[0]["commit"], "runs": len(rows),
                           "cases": len({r["case"] for r in rows})})
    index: dict = {"generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                   "rows": 0, "nights": {}, "builds": builds}
    for (night, job), rows in sorted(per_night.items()):
        night_dir = out / night
        night_dir.mkdir(exist_ok=True)
        with gzip.open(night_dir / f"{job}.jsonl.gz", "wt", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
        index["nights"].setdefault(night, {})[job] = {
            "runs": len(rows), "cases": len({r["case"] for r in rows}),
            "pass": sum(r["outcome"] == "pass" for r in rows),
            "fail": sum(r["outcome"] == "fail" for r in rows),
            "other": sum(r["outcome"] not in ("pass", "fail") for r in rows),
            "models": sorted({r["model"] for r in rows if r["model"]}),
        }
        index["rows"] += len(rows)
    (out / INDEX_FILE).write_text(json.dumps(index, indent=1, sort_keys=True))
    return index


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="write one JSONL per night and job from the cache")
    b.add_argument("--cache", required=True, type=pathlib.Path)
    b.add_argument("--out", required=True, type=pathlib.Path)
    args = ap.parse_args(argv)
    index = build(args.cache, args.out)
    nights = index["nights"]
    print(f"rows {index['rows']} nights {len(nights)} builds {len(index['builds'])}")
    for night in sorted(nights):
        parts = ", ".join(f"{job.replace('ci-kube-agents-eval-nightly', 'nightly')}: {v['cases']} cases {v['runs']} runs"
                          f" ({v['pass']}p/{v['fail']}f/{v['other']}o)" for job, v in sorted(nights[night].items()))
        print(f"  {night}  {parts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
