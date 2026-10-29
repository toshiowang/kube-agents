# Certified journeys and capabilities: the concept and the plan

Status: concept document, 2026-10-27. It states what we promise, what we measure, where the numbers stand, and the plan in phases. The detail sits in two companion documents: [`certified-journeys-technical-plan.md`](certified-journeys-technical-plan.md) (the fourteen steps, the measurement tables, the open decisions with their options, the review records) and [`certified-journeys-inventory.md`](certified-journeys-inventory.md) (the 47 journeys with evidence).

## 1. Summary

**The problem.** Customers ask for guarantees. An agent that runs on an AI model cannot promise the same outcome on every run. Today we publish neither a guarantee nor a measured rate. The product runs ten scheduled audits on every install, but no test grades what those scheduled runs produce, and only one skill has a proven pass record.

**The answer.** We publish a page of certified capabilities: for each model, what kube-agents can and cannot do today, computed from the nightly evaluation record. A capability is certified when it is evaluated on the published tests for it, on a named model, at the bar, with the record published. The same page states the one thing the product guarantees outside the model: the agent can only propose a change, never apply one.

**The moat.** The tests are not only ours. Each month the set grows with the top cases from Google Cloud Support: the failures customers actually hit, turned into tests with a planted defect and a check. The page therefore measures the product against real incidents, and no plain model or home-built agent is evaluated against that set.

**The two numbers we track.**

| Number                 | Meaning                                                                                              | Today                                                   | Target for 2026-12-14                                            |
| :--------------------- | :--------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------- |
| Unattended journeys    | Jobs the agent completes from a trigger to a result with no person in the loop, graded on the result | 17 can run this way; 0 are graded on their result       | 5 to 12 graded; 0 to 2 at the measured bar                       |
| Certified capabilities | Operator tasks with a proven pass record on a named model                                            | 1 of 21 tracked skills at the measured bar; 0 certified | 2 to 4 at the measured bar; the first certified line after 12-14 |

**The end state.** A customer opens a page on their own install and reads one line per journey and per model: the kind of promise, the pass rate, the dates, the exact version of the text the agent loaded, the difficulty level, and the typical cost in minutes and tokens. When a model update or a text edit breaks a journey, the next morning's page turns red and the owner receives an issue.

**What we need now.** Three decisions unblock the first phase: approval to tag each test with the skills it exercises, agreement to grade the five first-run audits on their real results inside the existing nightly, and a test project that can serve Claude.

**Words this document uses.**

| Word       | Meaning here                                                                                                                                                           |
| :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Journey    | A job the agent does for a customer, from a trigger to a result. Example: a critical access over-grant exists; by morning the agent has found it and proposed the fix. |
| Capability | One operator task the agent can do, with a nightly test. Example: grade a cluster's readiness for an upgrade.                                                          |
| Skill      | A package of rules and scripts the agent loads for one kind of task.                                                                                                   |
| Unattended | Started by a schedule or an event, and completed with no human step before the result.                                                                                 |
| Measured   | At least 57 of the newest 60 nightly runs passed, on one model and one exact version of the text.                                                                      |
| Certified  | Measured, plus a private test set, zero forbidden actions, a named model, and an outside reviewer who repeats the measurement.                                         |

## 2. Why a customer wants this

### 2.1 Preventive care, not the emergency room

Most Kubernetes AI tools work like an emergency room. An outage happens, a person is paged, and someone opens a chat window to diagnose it. Even a fast diagnosis comes after the damage. kube-agents is built as preventive care: scheduled check-ups that find weak points while the fleet is still healthy, with the fix written up and ready for signature before the incident.

| Preventive care                  | In kube-agents                                                                            |
| :------------------------------- | :---------------------------------------------------------------------------------------- |
| Scheduled check-up               | Ten audits that run on daily and weekly schedules                                         |
| Standard of care                 | 117 numbered checks, each with its exact condition, its severity and its fix              |
| Prescription ready for signature | A finding with evidence, paired with a proposed change that a person approves             |
| No surgery without consent       | Read-only access; every change needs a human approval                                     |
| Medical history                  | One tracking issue per audit, updated in place, with new, resolved and recurring findings |
| Pre-operative clearance          | Upgrade readiness graded per cluster before the upgrade                                   |
| Patient preference on file       | Exceptions the customer declares in Git are respected, not flagged                        |
| Paced communication              | At most two critical items a day; new alerts pause while earlier items await a decision   |

**Where this stands today.** The product schedules the check-up and grades the emergency room. By test volume it leans preventive: 11 of the 17 unattended journeys look for latent risk, and about 96 tests cover preventive work against about 23 for incident response. By pass rate the reactive side is more mature: crash and warning triage pass reliably, while the preventive audits carry most of the open defects. On the maintainers' own test install, 0 of the 18 fixes the audits proposed in the last 30 days were merged. We have not yet proved that operators fill the prescription.

### 2.2 Why not the model or agent you already run

**We do not replace your model. We give it a schedule, limits it cannot cross, and a nightly test record.**

A chat session acts only when prompted, runs with whatever credentials a user pastes in, and keeps no record on the customer's fleet. A home-built scheduled agent needs the team to build and maintain identity, write-blocking, fleet collectors, procedures and a test fleet. kube-agents ships six things in one:

1. **An operator's calendar and written procedures.** Scheduling a model is easy; writing and maintaining what runs on that schedule is not. The product ships ten scheduled audits, each with a numbered procedure, plus upgrade readiness checks, a stall watch, warning triage, in-place tracking issues, proposed fixes for critical findings, and paced notifications.
2. **Authority limits enforced outside the model.** Read-only access rights and a gateway that blocks every write hold whatever the prompt says. The worst outcome is a bad proposed change, never an unapproved change to a cluster.
3. **A regression tripwire.** Every night the shipped configuration runs 159 tests, three times each, against a seeded multi-cluster fleet. When a provider updates a model, a maintainer edits a prompt, or GKE changes an API, the break shows up the next morning in our test system rather than on a customer fleet. Today's tests plant one defect at a time, so this proves non-regression and authority, not deep troubleshooting skill (section 4.4).
4. **Executable GKE rules that age and get updated.** Wiki best practices rot because nothing executes them. The product encodes the perishable facts (release-channel versions, 52 deprecated or removed APIs, 33 version-specific known issues, version skew rules) into 117 audit checks and 24 upgrade-readiness rule modules. The customer can override any check by declaring intent in Git. Today 14 of the 15 governance procedures cite no published Google document; they encode maintainer practice. The plan adds a source line to every check and retires the rest (section 5).
5. **A record per model, so the customer can switch.** Journeys are rated per model. A customer can change models and read the line for the new one.
6. **A test set fed by Cloud Support.** Each month the top support cases become tests, so the nightly grades the product against the failures customers actually hit. A plain model is never evaluated against that set.

All execution stays in the customer's own cloud project, on their own model provider and billing account. Only the model prompts leave.

**Why vendor-backed rules matter.** Platform leads adopt vendor tooling partly for accountability: checks that trace to Google's published guidance, run by a Google-maintained product, produce a posture that support and security reviewers recognise at once. That holds only if every check really traces to published guidance and meets a high reliability bar. A false recommendation damages trust more than a missing check. The plan earns that bar rather than assumes it.

### 2.3 What customers asked for

From a retail platform team's requirements and the first-24-hour operating specification: pre-upgrade blockers and post-upgrade reviews first; detection of controllers that stop working without an error; audits that respect declared intent; a rating line for the exact model their install runs; proof that the agent never wrote to a cluster; tests the authors have not seen; a hard cap on noise; every fix as a proposed change they approve; and a warning from us before a regression reaches them.

## 3. What "certified" means here

### 3.1 The word problem

The industry uses "certified" for four unrelated things: a person's exam (CKA), a distribution's conformance ("Certified Kubernetes"), an organisation's control audit (SOC 2), and a partner badge. Customers hear "guaranteed". A model-driven agent cannot guarantee an outcome on every run, so we separate three promises and use a different word for each.

| Promise           | What it covers                                                                                                                                       | Strength of the claim                                               | Word we publish                                         |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------ |
| Guarantee         | The agent can only propose, never apply: read-only access rights and a gateway that blocks writes                                                    | A hard rule enforced outside the model, checked on every run        | guaranteed                                              |
| Measured rate     | How often a journey or task succeeds: the newest 60 nightly runs on a named model and exact text version, with an automatic drop when the rate falls | Statistical, like a service-level objective; never a single-run vow | measured                                                |
| Independent check | How the rate was produced: a private test set, zero forbidden actions, a named model, and an outside reviewer who repeats the number                 | Compliance-grade                                                    | certified, with its definition printed beside every use |

### 3.2 The ladder

Each step adds one condition that a customer or a reviewer can check without trusting the author.

| Step | Label                        | Evidence required                                                                                                                                                                                              | Count today                          |
| :--- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- |
| 0    | Claimed                      | Written in the documentation                                                                                                                                                                                   | 20 promises with no test             |
| 1    | Tested                       | At least one nightly test exists and has passed                                                                                                                                                                | Most journeys and skills             |
| 2    | Measured                     | At least 57 of the newest 60 nightly runs pass, on one model and one exact version of the text (24 of 24 while the window fills). The line drops when the rate falls below 0.70 on two nightly checks in a row | 1 skill (version control, on Claude) |
| 3    | Certified                    | Step 2, plus a private test set the authors never read, zero forbidden actions across the 60 runs, the named model and text version, and an outside reviewer who repeats the measurement                       | 0                                    |
| 3+   | Certified with measured lift | Step 3, plus the same tests run with the skill switched off, to show whether the skill helps, matches or hurts                                                                                                 | 0                                    |

The line a customer would read: "Certified: compliance audit on Claude Opus 5.5, since 2026-11-20, 60 of 60 on text version a1b2c3, private set 24 of 24, 0 forbidden actions in 60 runs, reviewed by <name>."

### 3.3 What gets certified

Journeys and capabilities get certified. Skills get an internal rating from the tests that use them. A pass counts whether or not the agent opened a skill: on Claude Opus 5.5, 9 of 11 cluster-level tests pass without the agent reading the skill text. The published line records what ran. Even when no skill text is read, the customer still gets the authority limit, the schedule, the fleet collectors, the nightly window and the drop alert.

Step 3 costs more than step 2: an isolated test project the authors cannot read, a private test suite (the review panel estimates it would double the nightly run volume), automated sweeps of the cloud and cluster audit logs, and a named outside reviewer. We adopt the definition now, at no cost, and fund the private project once the first journey reaches step 2.

## 4. What we measure, and against what

### 4.1 Pass or fail

A test places a known defect in a test fleet and checks that the agent reports it, in the tracking issue or in the proposed change. A paired test checks that the agent stays quiet about an exception the customer declared. 129 of the 230 tests place a defect, and 10 check silence on a clean posture. A model's own score of the agent's prose is recorded but never decides a pass. A test reads only what the product exports: the tracking issue, the proposed change, or the chat post. It never reads the scheduler's internal state, which proves only that a run started.

### 4.2 Authority

Any write to a cluster, any read of a secret, and any blocked write to the code repository fail the run. The end state adds a sweep of the cloud and cluster audit logs across every run in a window.

### 4.3 Reliability, cost and speed

Reliability is the 60-run window above. Minutes per run and tokens per run are recorded today and will be reported as a median and a 90th percentile per journey. We report them and do not gate on them: a slow run that produces the right fix is an expense, not a failure. We never publish a dollar figure, because the bill depends on the customer's provider; we publish the token counts and a per-model formula. Whether the agent follows the same route each night is not yet compared across runs; the plan adds bounds on the spread of steps, on repeated commands and on the spread of cost.

### 4.4 Difficulty levels

Most of today's 230 tests plant one defect on a four-cluster fleet and ask whether the agent names it. A capable model with a command line usually passes such a test on its own. Real operations problems are harder: a controller that stops with no error among 100 healthy workloads; a chain where a blocking admission webhook stalls a node drain, which stalls an upgrade, which strands a node pool; facts that change every month; ten clusters and 2,000 workloads inside a time budget; multi-day rollouts; a declared exception next to a real over-grant.

| Level | Problem                                                                        | What it tests                     | Where the product adds value                                           |
| :---- | :----------------------------------------------------------------------------- | :-------------------------------- | :--------------------------------------------------------------------- |
| 1     | One planted defect, graded by name                                             | Basic correctness and authority   | Little on reasoning; a bare model usually passes                       |
| 2     | Several signals with one misleading, declared exceptions, house severity rules | Judgment and rules                | The written procedures: severity, exceptions, silence on a clean fleet |
| 3     | Fleet scale, causal chains, multi-day horizons, perishable GKE facts           | Collectors, schedules, catalogues | Deterministic collectors, curated catalogues, unattended schedules     |

Today's record is almost all level 1, with a few level 2 tests and no active level 3 test. Every published line will name its level, and a level-1-only line will say so.

## 5. The plan

Three steps, in the order they add to the page.

### 5.1 Add the top Cloud Support cases to the nightly

Each month we take the top support cases and post-mortem patterns of the last 60 days, with no customer identifiers: the category, the symptom, the root cause, and whether a configuration change would have prevented it. We sort each pattern into one of five classes (not covered, covered but did not fire, caught with the wrong fix, knowledge missing, out of scope) and turn the top ones into tests: a planted defect on the test fleet and a check on the result. Today 129 of 230 tests plant defects we chose ourselves; the support cases are the failures customers hit. Done when the first batch of ten support-case tests runs nightly, the page shows which capability each strengthens, and a monthly line states what share of the top patterns a graded capability covers. Until a data agreement with Support exists, the loop runs on public known issues, release notes and the requirements of consenting customers.

### 5.2 Add the knowledge domains of the GKE and Kubernetes certification exams

The public curricula of the Kubernetes exams (KCNA, KCSA, CKA, CKAD, CKS) and the GKE parts of the Google Cloud exams (Associate Cloud Engineer, Professional Cloud Architect, Professional Cloud DevOps Engineer) are the industry's definition of what a qualified operator must know and do. We map every domain to a capability row, write a test for each domain the page does not cover, and run the performance-task domains (CKA, CKAD, CKS) on a scratch cluster where the agent proposes the change and the check reads the resulting state. The exam questions themselves stay confidential; the curricula and the community question banks are public. Done when every exam domain maps to a row or is marked out of scope, the first exam-domain tests run nightly, and the page states exam-domain coverage per model.

### 5.3 Make kube-agents pass the cases predictably

For every row below the bar we find the cause and fix it: a defect in the check (six known), a collector that misses the planted object (one), a rule the model walks past (four, moved into scripts or checks), a procedure that has no answer for a state (the weekly brief before its first review), or a missing fixture (the stall watch's positive case). Each fix runs red-to-green three times before it merges, and the record per model shows whether a fix on one model regresses another. Certified means predictable: a capability that passes 91 percent of runs is not one a customer can plan around. Done when the certified count per model rises each month and no row stays "Not yet" for two months without an owner and a date.

### 5.4 How progress is measured

The page is the scoreboard: the certified count per model; the number of rows strengthened by support cases and by exam domains; the plain-model column once the paired runs exist. The run store keeps every night, so every number on the page can be recomputed by anyone.

### 5.5 Risks

| Risk                                | Evidence                                                                                                         | Effect on the plan                                                                                            |
| :---------------------------------- | :--------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| No data agreement with Support yet  | The intake runs on public sources today                                                                          | Step 5.1 starts on public known issues and release notes; the support feed joins when the agreement is signed |
| A model switch restarts the record  | The nightly moved from Claude Opus 5.5 to Gemini 4 Argon on 10-29 and every window restarted                     | The page shows a column per model; a model with one night of record says so                                   |
| The nightly time budget             | About 100 tests fit in one job; a slower model pushes a lane past its ceiling                                    | Each new test needs a third job or a retired test; the paired runs run on our own installs                    |
| Exam tasks need a scratch cluster   | The performance-task domains change cluster state                                                                | Those tests run on a disposable cluster, never on the seeded fleet                                            |
| The model walks past a written rule | Four of the twelve low-scoring tests on Claude were the agent against a stated rule; four of those pass on Argon | Where the route matters, a script or a check enforces it; prose is never the only guard                       |

## Appendix. Sources

- The journeys, with evidence per row: [`certified-journeys-inventory.md`](certified-journeys-inventory.md).
- The fourteen steps, the tables, the decision options and the review records: [`certified-journeys-technical-plan.md`](certified-journeys-technical-plan.md).
- The counters: the local scorecard of 2026-10-27 and the nightly build logs of 10-23 to 10-27.
