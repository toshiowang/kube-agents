# What kube-agents can and cannot do today, on Gemini 4 Argon

Edition of 2026-11-03, computed from 2464 graded runs over 6 nights (2026-10-29 to 2026-11-03). Legend: ✅ Can = certified: 95 percent confidence of at least 85 percent pass on the row, no test below 80 percent; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model; 🔻 Lapsed = was certified, and the lower bound has been below 0.70 on two nightly checks in a row. 'Record since' beside a row counts every graded run on this model; the status reads the newest 60 per test.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 0.

**What certified means.** A capability is certified when, over the last three weeks of nightly runs, its tests pass at least 85 percent of the time with 95 percent confidence, and no single test falls below 80 percent. A regression shows within two nights. The exact rule: evaluated on the published tests for that capability, on a named model; the newest 60 graded runs per test; a 95 percent Wilson lower bound of at least 0.85 on the row (57 of 60 for a single test); no single test below 80 percent; the record published. Certified lapses when the lower bound sits below 0.70 on two nightly checks in a row.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 8 | 1 | 8 | 6 | 2 | 4 |

## Upgrades

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Upgrade readiness grades each cluster and names every blocker | scheduled, no person in the loop | 🟡 Mostly | 303 of 323 runs pass; lower bound 0.91; weakest test 13%; 3 listed tests never ran on this model; record since 2026-10-29: 303 of 323 |  |
| Patch readiness names the clusters behind on their version | scheduled, no person in the loop | ❌ Not yet | 0 of 28 runs pass; lower bound -0.00; weakest test 0%; record since 2026-10-29: 0 of 28 |  |
| Weekly readiness brief names the decisions a person owes | scheduled, no person in the loop | ✅ Can | 24 of 24 runs pass; lower bound 0.86; weakest test 100%; record since 2026-10-29: 24 of 24 |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | scheduled, no person in the loop | 🟠 Partly | 75 of 134 runs pass; lower bound 0.48; weakest test 0%; record since 2026-10-29: 75 of 134 |  |

## Incidents and troubleshooting

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | scheduled, no person in the loop | 🕒 Filling | no failure yet in 15 runs; the bar needs 24; record since 2026-10-29: 15 of 15 | only the silence side has a fixture |
| Warning event becomes a root cause, fix options and a pull request on "apply" | scheduled, no person in the loop | ✅ Can | 58 of 59 runs pass; lower bound 0.91; weakest test 93%; record since 2026-10-29: 58 of 59 |  |
| GitOps drift alert is triaged against the declared source | scheduled, no person in the loop | ✅ Can | 87 of 88 runs pass; lower bound 0.94; weakest test 93%; 1 listed test never ran on this model; record since 2026-10-29: 87 of 88 |  |
| Diagnose a broken workload without changing it | on request | 🟠 Partly | 62 of 78 runs pass; lower bound 0.69; weakest test 0%; record since 2026-10-29: 62 of 78 |  |
| Check observability wiring (metrics, traces, alerts) | on request | ✅ Can | 38 of 39 runs pass; lower bound 0.87; weakest test 92%; record since 2026-10-29: 38 of 39 |  |

## Security and compliance

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | scheduled, no person in the loop | 🟠 Partly | 42 of 57 runs pass; lower bound 0.61; weakest test 0%; record since 2026-10-29: 42 of 57 |  |
| AI security audit finds exposed model-serving workloads | scheduled, no person in the loop | 🟡 Mostly | 39 of 45 runs pass; lower bound 0.74; weakest test 73%; record since 2026-10-29: 39 of 45 |  |
| Networking fabric audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Reliability and capacity

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | scheduled, no person in the loop | ✅ Can | 67 of 69 runs pass; lower bound 0.90; weakest test 87%; record since 2026-10-29: 67 of 69 |  |
| Stockout prevention names node pools at risk | scheduled, no person in the loop | 🟠 Partly | 30 of 45 runs pass; lower bound 0.52; weakest test 0%; record since 2026-10-29: 30 of 45 | the collector misses the planted pool |
| Autoscaler stockout investigator | scheduled, no person in the loop | ⬜ No test | no test exists | off by default |

## Cost and consistency

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Cost audit finds idle resources and respects declared exceptions | scheduled, no person in the loop | 🟡 Mostly | 51 of 59 runs pass; lower bound 0.75; weakest test 60%; record since 2026-10-29: 51 of 59 |  |
| Consistency audit spots the cluster configured unlike its peers | scheduled, no person in the loop | 🟡 Mostly | 41 of 45 runs pass; lower bound 0.79; weakest test 80%; record since 2026-10-29: 41 of 45 |  |
| Compute fleet audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Changes and fixes

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Propose a change as a pull request, never apply it | on request | 🟡 Mostly | 68 of 74 runs pass; lower bound 0.83; weakest test 0%; record since 2026-10-29: 68 of 74 |  |
| Critical findings get a pull request, re-runs open no duplicate | scheduled, no person in the loop | ✅ Can | 56 of 56 runs pass; lower bound 0.94; weakest test 100%; record since 2026-10-29: 56 of 56 | the pull request is graded on request; the audit-opened one is not |
| Refuse an unsafe or direct change and name the safe path | on request | 🟡 Mostly | 77 of 96 runs pass; lower bound 0.71; weakest test 0%; record since 2026-10-29: 77 of 96 |  |
| Repository work (review replies, branch reuse, issue triage, forge commands) | on request | 🟡 Mostly | 77 of 83 runs pass; lower bound 0.85; weakest test 73%; 1 listed test never ran on this model; record since 2026-10-29: 77 of 83 |  |
| Repository watcher triages new issues | scheduled, no person in the loop | 🟠 Partly | 11 of 15 runs pass; lower bound 0.48; weakest test 73%; record since 2026-10-29: 11 of 15 |  |

## Working with the agent

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Converse well (answer first, say the next step, back claims with evidence) | on request | ❌ Not yet | 13 of 58 runs pass; lower bound 0.14; weakest test 0%; record since 2026-10-29: 13 of 58 |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | on request | ✅ Can | 24 of 24 runs pass; lower bound 0.86; weakest test 100%; 1 listed test never ran on this model; record since 2026-10-29: 24 of 24 |  |
| Run an audit now, or answer a fleet question from the collectors | on request | ✅ Can | 145 of 146 runs pass; lower bound 0.96; weakest test 93%; 2 listed tests never ran on this model; record since 2026-10-29: 145 of 146 |  |
| Answer GKE knowledge questions with sources | on request | 🟠 Partly | 75 of 95 runs pass; lower bound 0.70; weakest test 0%; record since 2026-10-29: 75 of 95 |  |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | scheduled, no person in the loop | ⬜ No test | no test exists | no evaluation install has a chat platform |
| First-run audits start at onboarding | scheduled, no person in the loop | 🟡 Mostly | 8 of 10 runs pass; lower bound 0.49; weakest test 80%; record since 2026-10-29: 8 of 10 |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
