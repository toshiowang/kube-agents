# What kube-agents can and cannot do today, on Claude Opus 5.5

Edition of 2026-11-04, computed from 2792 graded runs over 9 nights (2026-10-20 to 2026-10-28). Legend: ✅ Can = certified: 95 percent confidence of at least 85 percent pass on the row, no test below 80 percent; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model; 🔻 Lapsed = was certified, and the lower bound has been below 0.70 on two nightly checks in a row. 'Record since' beside a row counts every graded run on this model; the status reads the newest 60 per test.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 11.

**What certified means.** A capability is certified when, over the last three weeks of nightly runs, its tests pass at least 85 percent of the time with 95 percent confidence, and no single test falls below 80 percent. A regression shows within two nights. The exact rule: evaluated on the published tests for that capability, on a named model; the newest 60 graded runs per test; a 95 percent Wilson lower bound of at least 0.85 on the row (57 of 60 for a single test); no single test below 80 percent; the record published. Certified lapses when the lower bound sits below 0.70 on two nightly checks in a row.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 4 | 1 | 11 | 5 | 4 | 4 |

## Upgrades

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Upgrade readiness grades each cluster and names every blocker | scheduled, no person in the loop | 🟡 Mostly | 270 of 299 runs pass; lower bound 0.86; weakest test 0%; 3 listed tests never ran on this model; record since 2026-10-20: 270 of 299 |  |
| Patch readiness names the clusters behind on their version | scheduled, no person in the loop | ❌ Not yet | 4 of 35 runs pass; lower bound 0.05; weakest test 0%; record since 2026-10-20: 4 of 35 |  |
| Weekly readiness brief names the decisions a person owes | scheduled, no person in the loop | 🟠 Partly | 17 of 24 runs pass; lower bound 0.51; weakest test 22%; record since 2026-10-22: 17 of 24 |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | scheduled, no person in the loop | 🟠 Partly | 41 of 81 runs pass; lower bound 0.40; weakest test 0%; record since 2026-10-26: 41 of 81 |  |

## Incidents and troubleshooting

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | scheduled, no person in the loop | 🕒 Filling | no failure yet in 15 runs; the bar needs 24; record since 2026-10-20: 15 of 15 | only the silence side has a fixture |
| Warning event becomes a root cause, fix options and a pull request on "apply" | scheduled, no person in the loop | 🟡 Mostly | 78 of 93 runs pass; lower bound 0.75; weakest test 17%; record since 2026-10-20: 78 of 93 | autoops-quiet-followup: fixed by #3976 |
| GitOps drift alert is triaged against the declared source | scheduled, no person in the loop | 🟡 Mostly | 100 of 113 runs pass; lower bound 0.81; weakest test 56%; 1 listed test never ran on this model; record since 2026-10-20: 100 of 113 |  |
| Diagnose a broken workload without changing it | on request | 🟡 Mostly | 89 of 105 runs pass; lower bound 0.77; weakest test 0%; record since 2026-10-20: 89 of 105 |  |
| Check observability wiring (metrics, traces, alerts) | on request | ❌ Not yet | 22 of 48 runs pass; lower bound 0.33; weakest test 20%; record since 2026-10-20: 22 of 48 |  |

## Security and compliance

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | scheduled, no person in the loop | 🟡 Mostly | 71 of 78 runs pass; lower bound 0.83; weakest test 53%; record since 2026-10-20: 71 of 78 |  |
| AI security audit finds exposed model-serving workloads | scheduled, no person in the loop | 🟠 Partly | 40 of 65 runs pass; lower bound 0.49; weakest test 0%; record since 2026-10-20: 40 of 65 |  |
| Networking fabric audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Reliability and capacity

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | scheduled, no person in the loop | ✅ Can | 86 of 90 runs pass; lower bound 0.89; weakest test 87%; record since 2026-10-20: 86 of 90 |  |
| Stockout prevention names node pools at risk | scheduled, no person in the loop | 🟠 Partly | 36 of 60 runs pass; lower bound 0.47; weakest test 4%; record since 2026-10-20: 36 of 60 | the collector misses the planted pool |
| Autoscaler stockout investigator | scheduled, no person in the loop | ⬜ No test | no test exists | off by default |

## Cost and consistency

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Cost audit finds idle resources and respects declared exceptions | scheduled, no person in the loop | 🟡 Mostly | 60 of 65 runs pass; lower bound 0.83; weakest test 83%; record since 2026-10-20: 60 of 65 |  |
| Consistency audit spots the cluster configured unlike its peers | scheduled, no person in the loop | 🟡 Mostly | 50 of 62 runs pass; lower bound 0.69; weakest test 56%; record since 2026-10-20: 50 of 62 | drift-chat-request-runs-collector: fixed by #3609 |
| Compute fleet audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Changes and fixes

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Propose a change as a pull request, never apply it | on request | 🟡 Mostly | 131 of 162 runs pass; lower bound 0.74; weakest test 7%; record since 2026-10-20: 131 of 162 |  |
| Critical findings get a pull request, re-runs open no duplicate | scheduled, no person in the loop | ✅ Can | 81 of 81 runs pass; lower bound 0.95; weakest test 100%; record since 2026-10-20: 81 of 81 | the pull request is graded on request; the audit-opened one is not |
| Refuse an unsafe or direct change and name the safe path | on request | 🟠 Partly | 106 of 153 runs pass; lower bound 0.62; weakest test 13%; record since 2026-10-20: 106 of 153 | platform-worker-refuses-shipped-skill-edit: check fix in #4720 |
| Repository work (review replies, branch reuse, issue triage, forge commands) | on request | 🟡 Mostly | 151 of 156 runs pass; lower bound 0.93; weakest test 67%; record since 2026-10-20: 151 of 156 |  |
| Repository watcher triages new issues | scheduled, no person in the loop | ✅ Can | 27 of 27 runs pass; lower bound 0.88; weakest test 100%; record since 2026-10-20: 27 of 27 |  |

## Working with the agent

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Converse well (answer first, say the next step, back claims with evidence) | on request | ❌ Not yet | 29 of 63 runs pass; lower bound 0.34; weakest test 0%; record since 2026-10-20: 29 of 63 |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | on request | ❌ Not yet | 9 of 33 runs pass; lower bound 0.15; weakest test 0%; record since 2026-10-20: 9 of 33 | findings-decision-covers-item: Claude asks to confirm before a permanent dismissal; read-first 11-03, no fix yet |
| Run an audit now, or answer a fleet question from the collectors | on request | 🟡 Mostly | 159 of 175 runs pass; lower bound 0.86; weakest test 56%; 2 listed tests never ran on this model; record since 2026-10-20: 159 of 175 |  |
| Answer GKE knowledge questions with sources | on request | 🟡 Mostly | 90 of 111 runs pass; lower bound 0.73; weakest test 13%; record since 2026-10-20: 90 of 111 |  |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | scheduled, no person in the loop | ⬜ No test | no test exists | no evaluation install has a chat platform |
| First-run audits start at onboarding | scheduled, no person in the loop | ✅ Can | 27 of 27 runs pass; lower bound 0.88; weakest test 100%; record since 2026-10-20: 27 of 27 |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
