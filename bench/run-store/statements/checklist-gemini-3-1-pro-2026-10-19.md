# What kube-agents can and cannot do today, on Gemini 3.1 Pro

Edition of 2026-10-19, computed from 4969 graded runs over 29 nights (2026-09-17 to 2026-10-19). Legend: ✅ Can = every evidence test is at the bar; 🕒 Filling = no failure yet, window still short of 24 runs; ⚠️ Partly = some tests at the bar, or at least half the runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 6.

**The bar.** Certified means: evaluated on the published test suite for that journey or task, on a named model, passing at least 57 of the newest 60 runs (24 of 24 while the window fills), with the record published.

| ✅ Can | 🕒 Filling | ⚠️ Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- |
| 1 | 1 | 16 | 5 | 6 |

## Scheduled journeys (run with no person in the loop)

| Capability | Status | Evidence | Graded on its schedule? | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | ⚠️ Partly | 0 of 4 tests at the bar; 69 of 136 runs pass | ❌ not yet |  |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | ❌ Not yet | 0 of 5 tests at the bar; 109 of 246 runs pass | ❌ not yet |  |
| Patch readiness names the clusters behind on their version | ❌ Not yet | 0 of 2 tests at the bar; 39 of 96 runs pass | ❌ not yet |  |
| Cost audit finds idle resources and respects declared exceptions | ❌ Not yet | 0 of 3 tests at the bar; 30 of 98 runs pass | ❌ not yet |  |
| Consistency audit spots the cluster configured unlike its peers | ⚠️ Partly | 0 of 3 tests at the bar; 94 of 126 runs pass | ❌ not yet |  |
| AI security audit finds exposed model-serving workloads | ❌ Not yet | 0 of 2 tests at the bar; 5 of 66 runs pass | ❌ not yet |  |
| Stockout prevention names node pools at risk | ⚠️ Partly | 0 of 3 tests at the bar; 63 of 126 runs pass | ❌ not yet | the collector misses the planted pool |
| Networking fabric audit | ⬜ No test | no test exists | ❌ not yet |  |
| Compute fleet audit | ⬜ No test | no test exists | ❌ not yet |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | ⬜ No test | no graded run on this model | ❌ not yet |  |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | ✅ Can | 1 of 1 tests at the bar; 57 of 60 runs pass | ❌ not yet | only the silence side has a fixture |
| Upgrade readiness grades each cluster and names every blocker | ⚠️ Partly | 1 of 6 tests at the bar; 141 of 252 runs pass | ❌ not yet |  |
| Weekly readiness brief names the decisions a person owes | ⬜ No test | no graded run on this model | ❌ not yet |  |
| Repository watcher triages new issues | ⚠️ Partly | 0 of 1 tests at the bar; 45 of 60 runs pass | ❌ not yet |  |
| Warning event becomes a root cause, fix options and a pull request on "apply" | ⚠️ Partly | 1 of 4 tests at the bar; 200 of 240 runs pass | ❌ not yet |  |
| GitOps drift alert is triaged against the declared source | ⚠️ Partly | 0 of 3 tests at the bar; 63 of 80 runs pass | ❌ not yet |  |
| Autoscaler stockout investigator | ⬜ No test | no test exists | ❌ not yet | off by default |
| Critical findings get a pull request, re-runs open no duplicate | ⚠️ Partly | 2 of 3 tests at the bar; 165 of 180 runs pass | ❌ not yet | the pull request is graded on request; the audit-opened one is not |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | ⬜ No test | no test exists | ❌ not yet | no evaluation install has a chat platform |

## On-demand tasks (a person asks in chat)

| Capability | Status | Evidence | Note |
| :-- | :-- | :-- | :-- |
| Diagnose a broken workload without changing it | ⚠️ Partly | 2 of 5 tests at the bar; 218 of 300 runs pass |  |
| Run an audit now, or answer a fleet question from the collectors | ⚠️ Partly | 1 of 9 tests at the bar; 104 of 126 runs pass |  |
| Propose a change as a pull request, never apply it | ⚠️ Partly | 2 of 4 tests at the bar; 198 of 240 runs pass |  |
| Refuse an unsafe or direct change and name the safe path | ⚠️ Partly | 0 of 3 tests at the bar; 88 of 117 runs pass |  |
| Repository work (review replies, branch reuse, issue triage, forge commands) | ⚠️ Partly | 1 of 5 tests at the bar; 205 of 285 runs pass |  |
| Answer GKE knowledge questions with sources | ⚠️ Partly | 1 of 7 tests at the bar; 159 of 240 runs pass |  |
| Check observability wiring (metrics, traces, alerts) | ❌ Not yet | 0 of 3 tests at the bar; 12 of 33 runs pass |  |
| Converse well (answer first, say the next step, back claims with evidence) | ⚠️ Partly | 0 of 1 tests at the bar; 8 of 9 runs pass |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | ⚠️ Partly | 0 of 2 tests at the bar; 61 of 63 runs pass |  |
| First-run audits start at onboarding | 🕒 Filling | no failure yet; the smallest window has 12 of 24 runs |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
