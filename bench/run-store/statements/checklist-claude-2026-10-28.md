# What kube-agents can and cannot do today, on Claude Opus 5.5

Edition of 2026-10-28, computed from 2792 graded runs over 9 nights (2026-10-20 to 2026-10-28). Legend: ✅ Can = certified: 95 percent confidence of at least 85 percent pass on the row, no test below 80 percent; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 11.

**What certified means.** Certified means: evaluated on the published tests for that capability, on a named model, with 95 percent confidence that at least 85 percent of runs pass (57 of the newest 60 for a single test), no single test below 80 percent, and the record published.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 4 | 1 | 11 | 5 | 4 | 4 |

## Upgrades

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Upgrade readiness grades each cluster and names every blocker | scheduled, no person in the loop | 🟡 Mostly | 270 of 299 runs pass; lower bound 0.86; weakest test 0% |  |
| Patch readiness names the clusters behind on their version | scheduled, no person in the loop | ❌ Not yet | 4 of 35 runs pass; lower bound 0.05; weakest test 0% |  |
| Weekly readiness brief names the decisions a person owes | scheduled, no person in the loop | 🟠 Partly | 17 of 24 runs pass; lower bound 0.51; weakest test 22% |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | scheduled, no person in the loop | 🟠 Partly | 41 of 81 runs pass; lower bound 0.40; weakest test 0% |  |

## Incidents and troubleshooting

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | scheduled, no person in the loop | 🕒 Filling | no failure yet in 15 runs; the bar needs 24 | only the silence side has a fixture |
| Warning event becomes a root cause, fix options and a pull request on "apply" | scheduled, no person in the loop | 🟡 Mostly | 78 of 93 runs pass; lower bound 0.75; weakest test 17% |  |
| GitOps drift alert is triaged against the declared source | scheduled, no person in the loop | 🟡 Mostly | 100 of 113 runs pass; lower bound 0.81; weakest test 56% |  |
| Diagnose a broken workload without changing it | on request | 🟡 Mostly | 89 of 105 runs pass; lower bound 0.77; weakest test 0% |  |
| Check observability wiring (metrics, traces, alerts) | on request | ❌ Not yet | 22 of 48 runs pass; lower bound 0.33; weakest test 20% |  |

## Security and compliance

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | scheduled, no person in the loop | 🟡 Mostly | 71 of 78 runs pass; lower bound 0.83; weakest test 53% |  |
| AI security audit finds exposed model-serving workloads | scheduled, no person in the loop | 🟠 Partly | 40 of 65 runs pass; lower bound 0.49; weakest test 0% |  |
| Networking fabric audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Reliability and capacity

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | scheduled, no person in the loop | ✅ Can | 86 of 90 runs pass; lower bound 0.89; weakest test 87% |  |
| Stockout prevention names node pools at risk | scheduled, no person in the loop | 🟠 Partly | 36 of 60 runs pass; lower bound 0.47; weakest test 4% | the collector misses the planted pool |
| Autoscaler stockout investigator | scheduled, no person in the loop | ⬜ No test | no test exists | off by default |

## Cost and consistency

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Cost audit finds idle resources and respects declared exceptions | scheduled, no person in the loop | 🟡 Mostly | 60 of 65 runs pass; lower bound 0.83; weakest test 83% |  |
| Consistency audit spots the cluster configured unlike its peers | scheduled, no person in the loop | 🟡 Mostly | 50 of 62 runs pass; lower bound 0.69; weakest test 56% |  |
| Compute fleet audit | scheduled, no person in the loop | ⬜ No test | no test exists |  |

## Changes and fixes

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Propose a change as a pull request, never apply it | on request | 🟡 Mostly | 131 of 162 runs pass; lower bound 0.74; weakest test 7% |  |
| Critical findings get a pull request, re-runs open no duplicate | scheduled, no person in the loop | ✅ Can | 81 of 81 runs pass; lower bound 0.95; weakest test 100% | the pull request is graded on request; the audit-opened one is not |
| Refuse an unsafe or direct change and name the safe path | on request | 🟠 Partly | 106 of 153 runs pass; lower bound 0.62; weakest test 13% |  |
| Repository work (review replies, branch reuse, issue triage, forge commands) | on request | 🟡 Mostly | 151 of 156 runs pass; lower bound 0.93; weakest test 67% |  |
| Repository watcher triages new issues | scheduled, no person in the loop | ✅ Can | 27 of 27 runs pass; lower bound 0.88; weakest test 100% |  |

## Working with the agent

| Capability | Runs | Status | Evidence | Note |
| :-- | :-- | :-- | :-- | :-- |
| Converse well (answer first, say the next step, back claims with evidence) | on request | ❌ Not yet | 29 of 63 runs pass; lower bound 0.34; weakest test 0% |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | on request | ❌ Not yet | 9 of 33 runs pass; lower bound 0.15; weakest test 0% |  |
| Run an audit now, or answer a fleet question from the collectors | on request | 🟡 Mostly | 159 of 175 runs pass; lower bound 0.86; weakest test 56% |  |
| Answer GKE knowledge questions with sources | on request | 🟡 Mostly | 90 of 111 runs pass; lower bound 0.73; weakest test 13% |  |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | scheduled, no person in the loop | ⬜ No test | no test exists | no evaluation install has a chat platform |
| First-run audits start at onboarding | scheduled, no person in the loop | ✅ Can | 27 of 27 runs pass; lower bound 0.88; weakest test 100% |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
