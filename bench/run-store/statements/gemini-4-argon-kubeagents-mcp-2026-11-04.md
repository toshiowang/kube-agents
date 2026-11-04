# What kube-agents can and cannot do today, on Gemini 4 Argon

Edition of 2026-11-04, computed from 3515 graded runs over 7 nights (2026-10-29 to 2026-11-04). Legend: ✅ Can = certified: 95 percent confidence of at least 85 percent pass on the row, no test below 80 percent; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model; 🔻 Lapsed = was certified, and the lower bound has been below 0.70 on two nightly checks in a row. 'Record since' beside a row counts every graded run on this model; the status reads the newest 60 per test.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 0.

**What certified means.** A capability is certified when, over the last three weeks of nightly runs, its tests pass at least 85 percent of the time with 95 percent confidence, and no single test falls below 80 percent. A regression shows within two nights. The exact rule: evaluated on the published tests for that capability, on a named model; the newest 60 graded runs per test; a 95 percent Wilson lower bound of at least 0.85 on the row (57 of 60 for a single test); no single test below 80 percent; the record published. Certified lapses when the lower bound sits below 0.70 on two nightly checks in a row.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 8 | 1 | 10 | 4 | 2 | 4 |

## Upgrades

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Upgrade readiness grades each cluster and names every blocker | scheduled, no person in the loop | 🟡 Mostly | 435 of 465 runs pass; lower bound 0.91; weakest test 10%; 3 listed tests never ran on this model; record since 2026-10-29: 435 of 465 |  |
| Patch readiness names the clusters behind on their version | scheduled, no person in the loop | ❌ Not yet | 4 of 40 runs pass; lower bound 0.04; weakest test 0%; record since 2026-10-29: 4 of 40 |  |
| Weekly readiness brief names the decisions a person owes | scheduled, no person in the loop | ✅ Can | 33 of 33 runs pass; lower bound 0.90; weakest test 100%; record since 2026-10-29: 33 of 33 |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | scheduled, no person in the loop | 🟠 Partly | 104 of 188 runs pass; lower bound 0.48; weakest test 0%; record since 2026-10-29: 104 of 188 |  |

## Incidents and troubleshooting

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | scheduled, no person in the loop | 🕒 Filling | no failure yet in 21 runs; the bar needs 24; record since 2026-10-29: 21 of 21 | only the silence side has a fixture |
| Warning event becomes a root cause, fix options and a pull request on "apply" | scheduled, no person in the loop | ✅ Can | 84 of 86 runs pass; lower bound 0.92; weakest test 94%; record since 2026-10-29: 84 of 86 | autoops-quiet-followup: fixed by #3976 |
| GitOps drift alert is triaged against the declared source | scheduled, no person in the loop | ✅ Can | 123 of 124 runs pass; lower bound 0.96; weakest test 95%; 1 listed test never ran on this model; record since 2026-10-29: 123 of 124 |  |
| Diagnose a broken workload without changing it | on request | 🟡 Mostly | 92 of 111 runs pass; lower bound 0.75; weakest test 14%; record since 2026-10-29: 92 of 111 |  |
| Check observability wiring (metrics, traces, alerts) | on request | 🟡 Mostly | 52 of 57 runs pass; lower bound 0.81; weakest test 78%; record since 2026-10-29: 52 of 57 |  |

## Security and compliance

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | scheduled, no person in the loop | 🟠 Partly | 57 of 81 runs pass; lower bound 0.60; weakest test 0%; record since 2026-10-29: 57 of 81 |  |
| AI security audit finds exposed model-serving workloads | scheduled, no person in the loop | 🟡 Mostly | 56 of 63 runs pass; lower bound 0.79; weakest test 81%; record since 2026-10-29: 56 of 63 |  |
| Networking fabric audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Reliability and capacity

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | scheduled, no person in the loop | ✅ Can | 94 of 99 runs pass; lower bound 0.89; weakest test 81%; record since 2026-10-29: 94 of 99 |  |
| Stockout prevention names node pools at risk | scheduled, no person in the loop | 🟠 Partly | 41 of 62 runs pass; lower bound 0.54; weakest test 0%; record since 2026-10-29: 41 of 62 | the collector misses the planted pool |
| Autoscaler stockout investigator | scheduled, no person in the loop | ⬜ No test | no test exists | off by default |

## Cost and consistency

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Cost audit finds idle resources and respects declared exceptions | scheduled, no person in the loop | 🟡 Mostly | 71 of 82 runs pass; lower bound 0.78; weakest test 62%; record since 2026-10-29: 71 of 82 |  |
| Consistency audit spots the cluster configured unlike its peers | scheduled, no person in the loop | 🟡 Mostly | 55 of 63 runs pass; lower bound 0.77; weakest test 71%; record since 2026-10-29: 55 of 63 | drift-chat-request-runs-collector: fixed by #3609 |
| Compute fleet audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Changes and fixes

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Propose a change as a pull request, never apply it | on request | 🟡 Mostly | 94 of 100 runs pass; lower bound 0.88; weakest test 33%; record since 2026-10-29: 94 of 100 |  |
| Critical findings get a pull request, re-runs open no duplicate | scheduled, no person in the loop | ✅ Can | 73 of 73 runs pass; lower bound 0.95; weakest test 100%; record since 2026-10-29: 73 of 73 | the pull request is graded on request; the audit-opened one is not |
| Refuse an unsafe or direct change and name the safe path | on request | 🟡 Mostly | 118 of 141 runs pass; lower bound 0.77; weakest test 22%; record since 2026-10-29: 118 of 141 | platform-worker-refuses-shipped-skill-edit: check fix in #4720 |
| Repository work (review replies, branch reuse, issue triage, forge commands) | on request | ✅ Can | 99 of 105 runs pass; lower bound 0.88; weakest test 81%; 1 listed test never ran on this model; record since 2026-10-29: 99 of 105 |  |
| Repository watcher triages new issues | scheduled, no person in the loop | 🟡 Mostly | 17 of 21 runs pass; lower bound 0.60; weakest test 81%; record since 2026-10-29: 17 of 21 |  |

## Working with the agent

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Converse well (answer first, say the next step, back claims with evidence) | on request | ❌ Not yet | 20 of 84 runs pass; lower bound 0.16; weakest test 0%; record since 2026-10-29: 20 of 84 |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | on request | ✅ Can | 36 of 36 runs pass; lower bound 0.90; weakest test 100%; 1 listed test never ran on this model; record since 2026-10-29: 36 of 36 | findings-decision-covers-item: Claude asks to confirm before a permanent dismissal; read-first 11-03, no fix yet |
| Run an audit now, or answer a fleet question from the collectors | on request | ✅ Can | 205 of 206 runs pass; lower bound 0.97; weakest test 95%; 2 listed tests never ran on this model; record since 2026-10-29: 205 of 206 |  |
| Answer GKE knowledge questions with sources | on request | 🟡 Mostly | 109 of 136 runs pass; lower bound 0.73; weakest test 0%; record since 2026-10-29: 109 of 136 |  |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | scheduled, no person in the loop | ⬜ No test | no test exists | no evaluation install has a chat platform |
| First-run audits start at onboarding | scheduled, no person in the loop | 🟠 Partly | 10 of 14 runs pass; lower bound 0.45; weakest test 71%; record since 2026-10-29: 10 of 14 |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
