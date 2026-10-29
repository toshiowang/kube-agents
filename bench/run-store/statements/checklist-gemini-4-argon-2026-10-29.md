# What kube-agents can and cannot do today, on Gemini 4 Argon

Edition of 2026-10-29, computed from 503 graded runs over 1 nights (2026-10-29 to 2026-10-29). Legend: ✅ Can = certified: 95 percent confidence of at least 85 percent pass on the row, no test below 80 percent; 🕒 Filling = no failure yet, window still short of 24 runs; 🟡 Mostly = at least 80 percent of runs pass, below the bar; 🟠 Partly = between 50 and 79 percent of runs pass; ❌ Not yet = fewer than half the runs pass; ⬜ No test = no test, or none run on this model.

**Guaranteed.** The agent can only propose a change, never apply one: read-only access rights and a gateway that blocks writes. Cluster or repository writes caught by a safeguard in this record: 0. Other safeguard rules tripped (a card opened for an answer, a forbidden word, a sandbox tree check): 0.

**What certified means.** Certified means: evaluated on the published tests for that capability, on a named model, with 95 percent confidence that at least 85 percent of runs pass (57 of the newest 60 for a single test), no single test below 80 percent, and the record published.

| ✅ Can | 🕒 Filling | 🟡 Mostly | 🟠 Partly | ❌ Not yet | ⬜ No test |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | 12 | 3 | 7 | 2 | 4 |

## Scheduled journeys (run with no person in the loop)

| Capability | Status | Evidence | Graded on its schedule? | Note |
| :-- | :-- | :-- | :-- | :-- |
| Compliance audit finds risky access and respects declared exceptions | 🟠 Partly | 9 of 12 runs pass; lower bound 0.47; weakest test 0% | ❌ not yet |  |
| Reliability audit finds workloads that cannot survive maintenance, stays quiet on healthy ones | 🕒 Filling | no failure yet in 15 runs; the bar needs 24 | ❌ not yet |  |
| Patch readiness names the clusters behind on their version | ❌ Not yet | 0 of 4 runs pass; lower bound 0.00; weakest test 0% | ❌ not yet |  |
| Cost audit finds idle resources and respects declared exceptions | 🟠 Partly | 8 of 12 runs pass; lower bound 0.39; weakest test 0% | ❌ not yet |  |
| Consistency audit spots the cluster configured unlike its peers | 🕒 Filling | no failure yet in 9 runs; the bar needs 24 | ❌ not yet |  |
| AI security audit finds exposed model-serving workloads | 🟠 Partly | 6 of 9 runs pass; lower bound 0.35; weakest test 0% | ❌ not yet |  |
| Stockout prevention names node pools at risk | 🟠 Partly | 6 of 9 runs pass; lower bound 0.35; weakest test 0% | ❌ not yet | the collector misses the planted pool |
| Networking fabric audit | ⬜ No test | no test exists | ❌ not yet |  |
| Compute fleet audit | ⬜ No test | no test exists | ❌ not yet |  |
| Upgrade retrospective explains a failed upgrade, stays quiet after a clean week | 🟠 Partly | 15 of 27 runs pass; lower bound 0.37; weakest test 0% | ❌ not yet |  |
| Stall watch notices a controller that stopped, stays quiet on a healthy fleet | 🕒 Filling | no failure yet in 3 runs; the bar needs 24 | ❌ not yet | only the silence side has a fixture |
| Upgrade readiness grades each cluster and names every blocker | 🟡 Mostly | 73 of 77 runs pass; lower bound 0.87; weakest test 0% | ❌ not yet |  |
| Weekly readiness brief names the decisions a person owes | 🕒 Filling | no failure yet in 6 runs; the bar needs 24 | ❌ not yet |  |
| Repository watcher triages new issues | 🕒 Filling | no failure yet in 3 runs; the bar needs 24 | ❌ not yet |  |
| Warning event becomes a root cause, fix options and a pull request on "apply" | 🕒 Filling | no failure yet in 12 runs; the bar needs 24 | ❌ not yet |  |
| GitOps drift alert is triaged against the declared source | 🕒 Filling | no failure yet in 18 runs; the bar needs 24 | ❌ not yet |  |
| Autoscaler stockout investigator | ⬜ No test | no test exists | ❌ not yet | off by default |
| Critical findings get a pull request, re-runs open no duplicate | 🕒 Filling | no failure yet in 12 runs; the bar needs 24 | ❌ not yet | the pull request is graded on request; the audit-opened one is not |
| Chat posts (audit report, findings nudge, daily recap, fallback to the home channel) | ⬜ No test | no test exists | ❌ not yet | no evaluation install has a chat platform |

## On-demand tasks (a person asks in chat)

| Capability | Status | Evidence | Note |
| :-- | :-- | :-- | :-- |
| Diagnose a broken workload without changing it | 🟡 Mostly | 12 of 15 runs pass; lower bound 0.55; weakest test 0% |  |
| Run an audit now, or answer a fleet question from the collectors | ✅ Can | 30 of 30 runs pass; lower bound 0.89; weakest test 100% |  |
| Propose a change as a pull request, never apply it | 🕒 Filling | no failure yet in 12 runs; the bar needs 24 |  |
| Refuse an unsafe or direct change and name the safe path | 🟡 Mostly | 18 of 20 runs pass; lower bound 0.70; weakest test 33% |  |
| Repository work (review replies, branch reuse, issue triage, forge commands) | 🕒 Filling | no failure yet in 18 runs; the bar needs 24 |  |
| Answer GKE knowledge questions with sources | 🟠 Partly | 16 of 21 runs pass; lower bound 0.55; weakest test 0% |  |
| Check observability wiring (metrics, traces, alerts) | 🕒 Filling | no failure yet in 9 runs; the bar needs 24 |  |
| Converse well (answer first, say the next step, back claims with evidence) | ❌ Not yet | 4 of 13 runs pass; lower bound 0.13; weakest test 0% |  |
| Record a person's decision on a finding (dismiss, snooze, accept) | 🕒 Filling | no failure yet in 6 runs; the bar needs 24 |  |
| First-run audits start at onboarding | 🟠 Partly | 1 of 2 runs pass; lower bound 0.09; weakest test 50% |  |

## Not in this checklist

Twenty documented promises with no test, listed in `docs/designs/certified-journeys-inventory.md`; the dollar cost of a run; any comparison against a plain model, which the first paired run will add as a column.

## Method

Rows: `bench/run-store/capabilities.yaml`. Numbers: `bench/run-store/runs/`, the newest 60 graded runs per test on this model, 95 percent Wilson lower bound, not-applicable runs left out. Generator: `scripts/eval_dashboard/capability_checklist.py`.
