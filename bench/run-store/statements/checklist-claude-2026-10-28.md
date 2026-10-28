# What kube-agents can and cannot do today, on Claude Opus 5.5

Edition of 2026-10-28, computed from 2792 graded runs over 9 nights (2026-10-20 to 2026-10-28). Legend: ✅ Can = every evidence test is at the bar; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 11.

**What certified means.** Certified means: evaluated on the published test suite for that journey or task, on a named model, passing at least 57 of the newest 60 runs (24 of 24 while the window fills), with the record published.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 2 | 2 | 12 | 5 | 4 | 4 |

## Scheduled journeys (run with no person in the loop)

| Capability | Status | Evidence | Graded on its schedule? | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | 🟡 Mostly | 1 of 4 tests at the bar; 71 of 78 runs pass | ❌ not yet |  |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | 🟡 Mostly | 1 of 5 tests at the bar; 86 of 90 runs pass | ❌ not yet |  |
| Patch readiness names the clusters behind on their version | ❌ Not yet | 0 of 2 tests at the bar; 4 of 35 runs pass | ❌ not yet |  |
| Cost audit finds idle resources and respects declared exceptions | 🟡 Mostly | 0 of 4 tests at the bar; 60 of 65 runs pass | ❌ not yet |  |
| Consistency audit spots the cluster configured unlike its peers | 🟡 Mostly | 0 of 3 tests at the bar; 50 of 62 runs pass | ❌ not yet |  |
| AI security audit finds exposed model-serving workloads | 🟠 Partly | 1 of 3 tests at the bar; 40 of 65 runs pass | ❌ not yet |  |
| Stockout prevention names node pools at risk | 🟠 Partly | 0 of 3 tests at the bar; 36 of 60 runs pass | ❌ not yet | the collector misses the planted pool |
| Networking fabric audit | ⬜ No test | no test exists | ❌ not yet |  |
| Compute fleet audit | ⬜ No test | no test exists | ❌ not yet |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | 🟠 Partly | 0 of 9 tests at the bar; 41 of 81 runs pass | ❌ not yet |  |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | 🕒 Filling | no failure yet; the smallest window has 15 of 24 runs | ❌ not yet | only the silence side has a fixture |
| Upgrade readiness grades each cluster and names every blocker | 🟡 Mostly | 0 of 26 tests at the bar; 270 of 299 runs pass | ❌ not yet |  |
| Weekly readiness brief names the decisions a person owes | 🟠 Partly | 0 of 2 tests at the bar; 17 of 24 runs pass | ❌ not yet |  |
| Repository watcher triages new issues | ✅ Can | 1 of 1 tests at the bar; 27 of 27 runs pass | ❌ not yet |  |
| Warning event becomes a root cause, fix options and a pull request on "apply" | 🟡 Mostly | 1 of 5 tests at the bar; 78 of 93 runs pass | ❌ not yet |  |
| GitOps drift alert is triaged against the declared source | 🟡 Mostly | 0 of 6 tests at the bar; 100 of 113 runs pass | ❌ not yet |  |
| Autoscaler stockout investigator | ⬜ No test | no test exists | ❌ not yet | off by default |
| Critical findings get a pull request, re-runs open no duplicate | 🕒 Filling | no failure yet; the smallest window has 15 of 24 runs | ❌ not yet | the pull request is graded on request; the audit-opened one is not |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | ⬜ No test | no test exists | ❌ not yet | no evaluation install has a chat platform |

## On-demand tasks (a person asks in chat)

| Capability | Status | Evidence | Note |
| :-- | :-- | :-- | :-- |
| Diagnose a broken workload without changing it | 🟡 Mostly | 0 of 6 tests at the bar; 89 of 105 runs pass |  |
| Run an audit now, or answer a fleet question from the collectors | 🟡 Mostly | 1 of 10 tests at the bar; 159 of 175 runs pass |  |
| Propose a change as a pull request, never apply it | 🟡 Mostly | 2 of 6 tests at the bar; 131 of 162 runs pass |  |
| Refuse an unsafe or direct change and name the safe path | 🟠 Partly | 0 of 8 tests at the bar; 106 of 153 runs pass |  |
| Repository work (review replies, branch reuse, issue triage, forge commands) | 🟡 Mostly | 3 of 5 tests at the bar; 151 of 156 runs pass |  |
| Answer GKE knowledge questions with sources | 🟡 Mostly | 0 of 7 tests at the bar; 90 of 111 runs pass |  |
| Check observability wiring (metrics, traces, alerts) | ❌ Not yet | 0 of 3 tests at the bar; 22 of 48 runs pass |  |
| Converse well (answer first, say the next step, back claims with evidence) | ❌ Not yet | 0 of 5 tests at the bar; 29 of 63 runs pass |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | ❌ Not yet | 0 of 3 tests at the bar; 9 of 33 runs pass |  |
| First-run audits start at onboarding | ✅ Can | 1 of 1 tests at the bar; 27 of 27 runs pass |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
