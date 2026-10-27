# Run store

One row per eval run, every night, kept forever. A baseline is a named date range over these rows
(`baselines.yaml`); every aggregate (a 60-run window, a lower bound, a delta against a baseline)
is computed from the rows when asked, never stored as truth.

## Layout

- `runs/<night>/<job>.jsonl.gz`: one JSON object per repetition, for the nightly job that ran it
  (`ci-kube-agents-eval-nightly`, `-main-b`, `-writers`, `-gitlab`, `-today`). The night is the
  UTC date the Prow build started.
- `runs/index.json`: per night and job, the runs, cases, passes and fails, and the builds read.
- `baselines.yaml`: the named ranges.

Built by `scripts/eval_dashboard/run_store.py build --cache <dir> --out bench/run-store/runs` from
the artifacts `scripts/eval_dashboard/skill_use.py fetch` copies out of
`gs://kube-agents-evals-nightly-logs/logs/<job>/<build>/artifacts/` (`case-*.json`,
`results_<case>_rep<n>.json`, the run directories). The raw artifacts stay in that bucket and in
the local cache; this store carries the structured part.

## One row

| Field | Meaning |
| --- | --- |
| `night`, `job`, `build`, `commit` | When, which lane, which Prow build, which `main` commit it tested |
| `case`, `domain`, `rep`, `run_dir`, `results_file` | The test, its domain, the repetition (1 to 3) and the artifacts it came from |
| `outcome`, `reason`, `rung` | `pass`, `fail` or `not_applicable`, the one-line reason, the ladder rung that stopped it |
| `expected_fail`, `admitted`, `record_verdict` | The case's declared marker, its roster admission, the night's record verdict |
| `model`, `model_id`, `scoring_version`, `judge_model`, `fleet`, `verifiers`, `mode` | The version key the run was measured at; `model_id` is the served model from the run manifest |
| `latency_s`, `turn1_s` | Seconds for the run and for its first turn |
| `tokens`, `tokens_by_agent` | Input, cached, cache-write, reasoning, output, total; the worker roll-up when the top level is empty; totals per agent |
| `judged`, `correctness`, `coverage`, `catastrophic` | The judge's three scores and the deterministic ratios; informational, never a pass |
| `checks`, `check_counts`, `not_applicable_checks` | Every check's name, role, status, success, severity and a short reason; the counts per role and status |
| `tools`, `tool_calls`, `skills_opened` | Distinct tool names, the number of trajectory steps, the skills the agent opened with `skill_view` |
| `grader` | `as-recorded` for the nightly's own verdict; a later re-grade adds rows with its own grader name and leaves these |

## Rules

- Append-only. A night's file is rebuilt only from the same immutable artifacts. A check fix never
  edits a row; it adds re-graded rows under a new `grader`.
- A comparison uses one grader on both sides.
- Nights with no file had no recorded cases (the nightly died before `finish_case`, or did not run).
