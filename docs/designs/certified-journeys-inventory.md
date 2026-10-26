# Journey inventory for the certified-journeys design (2026-10-26)

Basis: `upstream/main` 791b1c102; untracked `first-24-hour.md` and `first-24-hour-gaps.md` from the working tree.
Readiness: **now** = zero human steps after the trigger and a live journey test or release pipeline green end to end
on a stock install today; **near** = one human step, or shipped but proven only by bench tasks on the eval fleet, or by
a CUJ whose evidence criteria fail closed on a stock install, or shipped and unverified; **far** = design or
infrastructure missing. Abbreviations: NC = `hack/eval/nightly-cases.txt`, PS = `hack/eval/presubmit-cases.txt`,
BR = `hack/eval/blocking-roster.txt`, VBC = `scripts/validate_bench_cases.py`, DY = `docs/designs/domains.yaml`.

Companion to [`certified-journeys-and-capabilities.md`](certified-journeys-and-capabilities.md).

## Counts

| measure                                                                | count | rows                                                                                                                                                                                 |
| ---------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| journeys inventoried                                                   | 47    | 10 AUD, 11 WATCH, 3 EVT, 4 ONB, 18 CHAT, 1 REM                                                                                                                                       |
| readiness now                                                          | 0     | none meets "zero human steps + green live journey test on a stock install"                                                                                                           |
| readiness near                                                         | 44    | all AUD, all WATCH, EVT-01, EVT-02, all ONB, CHAT-01..05, 08..18, REM-01                                                                                                             |
| readiness far                                                          | 3     | EVT-03 (stockout investigator, off by default), CHAT-06 (CUJ4 re-check into the thread), CHAT-07 (CUJ5 reactive re-plan)                                                             |
| of the 44 near: shipped with no verification at all                    | 7     | AUD-08 networking, AUD-09 GCE, WATCH-05 sa-role, WATCH-06 chat-delivery, WATCH-07 kanban health, WATCH-08 daily recap, WATCH-09 feedback prompt                                      |
| zero human steps between trigger and stated outcome                    | 42    | all AUD (10), all WATCH (11), EVT-01..03 (3), CHAT-01..14, 16..18 (17), REM-01                                                                                                       |
| a human step before the outcome                                        | 5     | ONB-01..04 (installer, first message, scripts), CHAT-15 (`/feedback` confirm)                                                                                                        |
| zero-step journeys whose next step is a human reply or merge by design | 7     | WATCH-01 (`apply`), WATCH-03/04 (decide), EVT-01 (`apply` unless `INCIDENT_TRIAGE_OPEN_PULL_REQUEST=true`), EVT-02 (reply), CHAT-10/REM-01 (merge), CHAT-16 (operator runs upgrades) |

## The 25 HOOTL-capable journeys (non-human trigger)

| id       | journey                                       | trigger                                  | verified today                                                                                                                                                                      | owner                                   |
| -------- | --------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| AUD-01   | compliance-audit                              | daily 06:20 UTC; once at onboarding      | 5 cases (`compliance-rbac-overgrant` held out; `compliance-declared-intent-no-finding`, `-token-shields-siblings`, `security-chat-request-runs-collector`, `oobe-first-run-audits`) | security jayantid; machinery toshiowang |
| AUD-02   | obtainability-audit (reliability)             | daily 06:50; onboarding                  | 8 cases incl. `obtainability-planted-pdb`; auto-PR case FIXTURE_NOT_READY                                                                                                           | reliability stalhaali                   |
| AUD-03   | security-patch-orchestrator                   | weekly Mon 07:20                         | 7 cases                                                                                                                                                                             | upgrades haoxuw                         |
| AUD-04   | fleet-wide-cost-analysis                      | weekly Mon 07:50; onboarding             | 5 cases                                                                                                                                                                             | cost Fuxiao-Gao                         |
| AUD-05   | fleet-consistency-drift                       | weekly Mon 08:20                         | 4 cases, no presubmit seat                                                                                                                                                          | consistency lapis2002                   |
| AUD-06   | ai-security-audit                             | daily 08:50                              | 3 cases                                                                                                                                                                             | security jayantid                       |
| AUD-07   | stockout-prevention                           | daily 09:20; onboarding                  | 5 cases                                                                                                                                                                             | capacity haoxuw                         |
| AUD-08   | gcp-networking-fabric-audit                   | daily 08:00                              | nothing registered                                                                                                                                                                  | no domain row (fleet-audits)            |
| AUD-09   | gce-compute-fleet-audit                       | daily 07:45                              | nothing registered                                                                                                                                                                  | no domain row (fleet-audits)            |
| AUD-10   | upgrade-retrospective                         | weekly Sun 18:00; onboarding; on request | 10 cases; after-upgrade trigger not built                                                                                                                                           | upgrades haoxuw                         |
| WATCH-01 | stall watch to Cluster Agent triage           | every 30 min                             | 2 cases; positive diagnosis case FIXTURE_NOT_READY                                                                                                                                  | incident-triage stalhaali               |
| WATCH-02 | upgrade-readiness watch                       | daily 10:10                              | no case names the job; the skill it runs has many                                                                                                                                   | upgrades haoxuw                         |
| WATCH-03 | weekly upgrade readiness review and brief     | Sat 06:00 / 07:00                        | 2 cases                                                                                                                                                                             | upgrades haoxuw                         |
| WATCH-04 | findings nudge, paced                         | hourly                                   | 2 cases                                                                                                                                                                             | fleet-audits toshiowang                 |
| WATCH-05 | sa-role watch                                 | hourly                                   | nothing                                                                                                                                                                             | security jayantid                       |
| WATCH-06 | chat-delivery watch                           | every 30 min                             | nothing                                                                                                                                                                             | fleet-audits toshiowang                 |
| WATCH-07 | kanban board health                           | daily 12:35                              | nothing                                                                                                                                                                             | chat-and-routing toshiowang             |
| WATCH-08 | event-watcher daily recap                     | weekdays 21:00                           | nothing                                                                                                                                                                             | observability bradhoekstra              |
| WATCH-09 | feedback prompt                               | once, day 7                              | nothing                                                                                                                                                                             | chat-and-routing toshiowang             |
| WATCH-10 | Cluster Agent reconcile                       | hourly                                   | 1 case reads the roster; none plants a new cluster                                                                                                                                  | cluster-debugging bradhoekstra          |
| WATCH-11 | repo watcher, issue resolver, PR conversation | every 10 min                             | 2 cases; live validation recorded                                                                                                                                                   | source-control dshnayder                |
| EVT-01   | warning event, triage, `apply`, PR            | cluster event                            | 8 cases; no-reply PR path FIXTURE_NOT_READY                                                                                                                                         | incident-triage stalhaali               |
| EVT-02   | GitOps drift alert and triage                 | audit log via Pub/Sub                    | 5 cases                                                                                                                                                                             | incident-triage stalhaali               |
| EVT-03   | autoscaler stockout investigator              | Cloud Logging alert                      | nothing; off by default                                                                                                                                                             | capacity haoxuw                         |
| REM-01   | audit remediation cycle                       | audit run                                | 3 ledger cases; no case grades an auto-opened PR or a merge                                                                                                                         | remediation Fuxiao-Gao                  |

## Promises in the docs with no journey test and no registered case (20 rows, summary)

The scheduled path itself; silence on a clean fleet; the auto-opened remediation PR and the merge that resolves it;
networking and GCE audits; audits without a GitOps repository; Slack cards and buttons; the no-reply incident PR;
`FailedScaleUp` reactive triage; "run it now" from chat; the eleven lesser watches and the hourly reconcile of a new
cluster; the T+5 single-command install; T+0 agent-initiated conversation; the scheduled deprecated-API scan; storage,
TLS, CVE, RBAC-change, Ingress 502, incident summary, WI validation, Dataplane V2 items of the first-24-hour spec; the
triage cascade skill and self-refinement; multi-project scope; "stays inside its own cluster"; CUJ1/CUJ3 evidence
criteria on a stock install; CUJ4 and CUJ5.

## Notes

- `first-24-hour-gaps.md` is pinned to 5e18d111 (2026-09-24) and stale on rows now built (findings pacing, first-run
  audits at onboarding, `INCIDENT_TRIAGE_OPEN_PULL_REQUEST`, stall watch, upgrade-readiness watch, sa-role watch, `/feedback`).
- `bench/cuj/` is a manual tier by design; every journey needs a live install and the READY preflight; owner haoxuw.
- The presubmit grades `spec.mode: next` through the inject lane; 20 chat cases and `agent-kanban-smoke` are graded
  only in the nightlies.
- Every case is `validated: false` except two.
- Domains uncovered in presubmit: fleet-audits, remediation, consistency, observability.
