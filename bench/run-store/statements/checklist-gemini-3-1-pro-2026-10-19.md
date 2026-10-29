# What kube-agents can and cannot do today, on Gemini 3.1 Pro

Edition of 2026-10-19, computed from 4969 graded runs over 29 nights (2026-09-17 to 2026-10-19). Legend: ✅ Can = certified: 95 percent confidence of at least 85 percent pass on the row, no test below 80 percent; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 6.

**What certified means.** Certified means: evaluated on the published tests for that capability, on a named model, with 95 percent confidence that at least 85 percent of runs pass (57 of the newest 60 for a single test), no single test below 80 percent, and the record published.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 2 | 1 | 5 | 10 | 5 | 6 |

## Upgrades

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Upgrade readiness grades each cluster and names every blocker | scheduled, no person in the loop | 🟠 Partly | 141 of 252 runs pass; lower bound 0.50; weakest test 33% |  |
| Patch readiness names the clusters behind on their version | scheduled, no person in the loop | ❌ Not yet | 39 of 96 runs pass; lower bound 0.31; weakest test 6% |  |
| Weekly readiness brief names the decisions a person owes | scheduled, no person in the loop | ⬜ No test | no graded run on this model |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | scheduled, no person in the loop | ⬜ No test | no graded run on this model |  |

## Incidents and troubleshooting

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | scheduled, no person in the loop | ✅ Can | 57 of 60 runs pass; lower bound 0.86; weakest test 95% | only the silence side has a fixture |
| Warning event becomes a root cause, fix options and a pull request on "apply" | scheduled, no person in the loop | 🟡 Mostly | 200 of 240 runs pass; lower bound 0.78; weakest test 55% |  |
| GitOps drift alert is triaged against the declared source | scheduled, no person in the loop | 🟠 Partly | 63 of 80 runs pass; lower bound 0.69; weakest test 0% |  |
| Diagnose a broken workload without changing it | on request | 🟠 Partly | 218 of 300 runs pass; lower bound 0.67; weakest test 20% |  |
| Check observability wiring (metrics, traces, alerts) | on request | ❌ Not yet | 12 of 33 runs pass; lower bound 0.22; weakest test 10% |  |

## Security and compliance

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | scheduled, no person in the loop | 🟠 Partly | 69 of 136 runs pass; lower bound 0.42; weakest test 44% |  |
| AI security audit finds exposed model-serving workloads | scheduled, no person in the loop | ❌ Not yet | 5 of 66 runs pass; lower bound 0.03; weakest test 0% |  |
| Networking fabric audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Reliability and capacity

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | scheduled, no person in the loop | ❌ Not yet | 109 of 246 runs pass; lower bound 0.38; weakest test 18% |  |
| Stockout prevention names node pools at risk | scheduled, no person in the loop | 🟠 Partly | 63 of 126 runs pass; lower bound 0.41; weakest test 2% | the collector misses the planted pool |
| Autoscaler stockout investigator | scheduled, no person in the loop | ⬜ No test | no test exists | off by default |

## Cost and consistency

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Cost audit finds idle resources and respects declared exceptions | scheduled, no person in the loop | ❌ Not yet | 30 of 98 runs pass; lower bound 0.22; weakest test 22% |  |
| Consistency audit spots the cluster configured unlike its peers | scheduled, no person in the loop | 🟠 Partly | 94 of 126 runs pass; lower bound 0.66; weakest test 0% |  |
| Compute fleet audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Changes and fixes

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Propose a change as a pull request, never apply it | on request | 🟡 Mostly | 198 of 240 runs pass; lower bound 0.77; weakest test 55% |  |
| Critical findings get a pull request, re-runs open no duplicate | scheduled, no person in the loop | 🟡 Mostly | 165 of 180 runs pass; lower bound 0.87; weakest test 78% | the pull request is graded on request; the audit-opened one is not |
| Refuse an unsafe or direct change and name the safe path | on request | 🟠 Partly | 88 of 117 runs pass; lower bound 0.67; weakest test 0% |  |
| Repository work (review replies, branch reuse, issue triage, forge commands) | on request | 🟠 Partly | 205 of 285 runs pass; lower bound 0.66; weakest test 2% |  |
| Repository watcher triages new issues | scheduled, no person in the loop | 🟠 Partly | 45 of 60 runs pass; lower bound 0.63; weakest test 75% |  |

## Working with the agent

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Converse well (answer first, say the next step, back claims with evidence) | on request | 🟡 Mostly | 8 of 9 runs pass; lower bound 0.57; weakest test 89% |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | on request | ✅ Can | 61 of 63 runs pass; lower bound 0.89; weakest test 95% |  |
| Run an audit now, or answer a fleet question from the collectors | on request | 🟡 Mostly | 104 of 126 runs pass; lower bound 0.75; weakest test 0% |  |
| Answer GKE knowledge questions with sources | on request | 🟠 Partly | 159 of 240 runs pass; lower bound 0.60; weakest test 4% |  |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | scheduled, no person in the loop | ⬜ No test | no test exists | no evaluation install has a chat platform |
| First-run audits start at onboarding | scheduled, no person in the loop | 🕒 Filling | no failure yet in 12 runs; the bar needs 24 |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
