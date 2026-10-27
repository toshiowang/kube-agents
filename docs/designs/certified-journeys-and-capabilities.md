# Certified journeys and capabilities: the concept and the plan

Status: concept document, 2026-10-27. It states what we promise, what we measure, where the numbers stand, and the plan in phases. The detail sits in two companion documents: [`certified-journeys-technical-plan.md`](certified-journeys-technical-plan.md) (the fourteen steps, the measurement tables, the open decisions with their options, the review records) and [`certified-journeys-inventory.md`](certified-journeys-inventory.md) (the 47 journeys with evidence). Tracking issue: [#3978](https://github.com/gke-labs/kube-agents/issues/3978).

## 1. Summary

**The problem.** Customers ask for guarantees. An agent that runs on an AI model cannot promise the same outcome on every run. Today we publish neither a guarantee nor a measured rate. The product runs ten scheduled audits on every install, but no test grades what those scheduled runs produce, and only one skill has a proven pass record.

**The answer.** We make three kinds of promise and keep them apart. We **guarantee** what the product enforces outside the model: the agent can only propose a change, never apply one. We **measure** how often each journey and each task succeeds, every night, on a named model, and we publish the rate with its dates. We call a line **certified** only when a reviewer outside the team has repeated the measurement on tests the authors never saw.

**The two numbers we track.**

| Number                 | Meaning                                                                                              | Today                                                   | Target for 2026-12-14                                            |
| :--------------------- | :--------------------------------------------------------------------------------------------------- | :------------------------------------------------------ | :--------------------------------------------------------------- |
| Unattended journeys    | Jobs the agent completes from a trigger to a result with no person in the loop, graded on the result | 17 can run this way; 0 are graded on their result       | 5 to 12 graded; 0 to 2 at the measured bar                       |
| Certified capabilities | Operator tasks with a proven pass record on a named model                                            | 1 of 21 tracked skills at the measured bar; 0 certified | 2 to 4 at the measured bar; the first certified line after 12-14 |

**The end state.** A customer opens a page on their own install and reads one line per journey and per model: the kind of promise, the pass rate, the dates, the exact version of the text the agent loaded, the difficulty level, and the typical cost in minutes and tokens. When a model update or a text edit breaks a journey, the next morning's page turns red and the owner receives an issue.

**What we need now.** Three decisions unblock the first phase: approval to tag each test with the skills it exercises, agreement to grade the five first-run audits on their real results inside the existing nightly, and a test project that can serve Claude. Five larger decisions stay parked until this concept is agreed (section 7.4).

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

**The honest state.** The product schedules the check-up and grades the emergency room. By test volume it leans preventive: 11 of the 17 unattended journeys look for latent risk, and about 96 tests cover preventive work against about 23 for incident response. By pass rate the reactive side is more mature: crash and warning triage pass reliably, while the preventive audits carry most of the open defects. On the maintainers' own test install, 0 of the 18 fixes the audits proposed in the last 30 days were merged. We have not yet proved that operators fill the prescription.

### 2.2 Why not a chat window or a home-built agent

A chat session acts only when prompted, runs with whatever credentials a user pastes in, and keeps no record on the customer's fleet. A home-built scheduled agent needs the team to build and maintain identity, write-blocking, fleet collectors, procedures and a test fleet. kube-agents ships five things in one:

1. **An operator's calendar and written procedures.** Scheduling a model is easy; writing and maintaining what runs on that schedule is not. The product ships ten scheduled audits, each with a numbered procedure, plus upgrade readiness checks, a stall watch, warning triage, in-place tracking issues, proposed fixes for critical findings, and paced notifications.
2. **Authority limits enforced outside the model.** Read-only access rights and a gateway that blocks every write hold whatever the prompt says. The worst outcome is a bad proposed change, never an unapproved change to a cluster.
3. **A regression tripwire.** Every night the shipped configuration runs 159 tests, three times each, against a seeded multi-cluster fleet. When a provider updates a model, a maintainer edits a prompt, or GKE changes an API, the break shows up the next morning in our test system rather than on a customer fleet. Today's tests plant one defect at a time, so this proves non-regression and authority, not deep troubleshooting skill (section 4.4).
4. **Executable GKE rules that age and get updated.** Wiki best practices rot because nothing executes them. The product encodes the perishable facts (release-channel versions, 52 deprecated or removed APIs, 33 version-specific known issues, version skew rules) into 117 audit checks and 24 upgrade-readiness rule modules. The customer can override any check by declaring intent in Git. Today 14 of the 15 governance procedures cite no published Google document; they encode maintainer practice. The plan adds a source line to every check and retires the rest (section 6.4).
5. **A record per model, so the customer can switch.** Journeys are rated per model. A customer can change models and read the line for the new one.

All execution stays in the customer's own cloud project, on their own model provider and billing account. Only the model prompts leave.

**Why vendor-backed rules matter.** Platform leads adopt vendor tooling partly for accountability: checks that trace to Google's published guidance, run by a Google-maintained product, produce a posture that support and security reviewers recognise at once. That holds only if every check really traces to published guidance and meets a high reliability bar. A false recommendation damages trust more than a missing check. The plan earns that bar rather than assumes it.

### 2.3 What customers asked for

From the retail customer epic [#2597](https://github.com/gke-labs/kube-agents/issues/2597) and the first-24-hour operating specification: pre-upgrade blockers and post-upgrade reviews first; detection of controllers that stop working without an error; audits that respect declared intent; a rating line for the exact model their install runs; proof that the agent never wrote to a cluster; tests the authors have not seen; a hard cap on noise; every fix as a proposed change they approve; and a warning from us before a regression reaches them.

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

### 4.5 Comparisons

| Question                                         | Baseline                                                                                                                  | State                                                                                                      |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------- |
| Which model is best on each journey?             | The same tests on two models inside the product                                                                           | Measured. Across 14 shared skills, Claude Opus 5.5 leads Gemini 3.1 Pro on 5, trails on 5 and ties on 4.   |
| How much does the product add over a bare model? | The same tests with the skill switched off; a pilot on public exam tasks against a bare model with the same cluster tools | Not measured end to end. Earlier work on Gemini found no lift from skill prose in 5 of 7 suites.           |
| Do skills help a strong model?                   | Pass rates with the skill opened against unopened                                                                         | Equal on Claude for the prose; the rules and scripts carry the value. A control run per model will decide. |
| Does it match a competent operator?              | A GKE engineer runs the same journey by hand once                                                                         | Not measured; proposed for the first four or five audits                                                   |
| Does it catch real incidents?                    | Customer failures, starting with the retail epic, turned into tests                                                       | Planned                                                                                                    |

### 4.6 Effectiveness beyond the tests

| Measure                                    | Today                                                                                                          | Path                                                                                                    |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| Known defects found                        | High on single checks; low on full audits (the compliance audit end to end passes 0.21 on Claude over 34 runs) | Nightly tests                                                                                           |
| False findings                             | Declared exceptions pass 9 of 9; a clean full fleet is untested                                                | Add a clean fleet to the test pool                                                                      |
| Proposed fixes merged                      | 0 of 18 in 30 days on the test install                                                                         | Grade whether the proposed change fixes the defect and passes its checks; track merges on live installs |
| Findings acted on                          | Stored per install, not summed                                                                                 | A summary over the findings queue                                                                       |
| Time to first finding                      | Measured per test, not shown as a product number                                                               | Extract it from the onboarding record                                                                   |
| Incidents caught before a person was paged | Not measured                                                                                                   | Needs a fleet with an incident log                                                                      |

## 5. Where we are today (2026-10-27)

| Counter                                               | Value                                                                                                                 |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| Journeys documented                                   | 47                                                                                                                    |
| Journeys that can run unattended                      | 17: ten scheduled audits, three watches that hand work to an agent, three event-driven flows, one fix cycle           |
| Unattended journeys with the scheduled start graded   | 5                                                                                                                     |
| Unattended journeys with the scheduled result graded  | 0                                                                                                                     |
| Unattended journeys graded in part by on-demand tests | 14 of 17                                                                                                              |
| Documented promises with no test                      | 20                                                                                                                    |
| Tests                                                 | 230, of which 159 run every night, three times each                                                                   |
| Nightly record                                        | 158 of 159 tests recorded on 10-27, after the nightly was split in two; the three nights before recorded 22, 0 and 26 |
| Skills                                                | 53 shipped; 23 named by no test; 1 at the measured bar (version control on Claude, 57 of 57 since 10-25)              |
| Journeys whose chat result can be graded              | 0                                                                                                                     |

Four causes sit behind these numbers. The nightly pauses the clock-started audits during its run, except the five first-run audits, and no test reads what a scheduled run produced. No test install has a chat platform, so a chat post cannot be graded. The nightly ran past its time budget until the split on 10-27, and about 100 tests fit in one 12-hour job. The checks were validated on one model, and eight of them broke when the nightly moved to Claude.

## 6. How it works at the end state

### 6.1 What the customer sees

A page on their own install lists one line per journey and per model: the kind of promise, the pass rate and its lower bound, the dates, the exact version of the text the agent loaded, the difficulty level, the typical cost in minutes and tokens, the skills read during the runs, and the most recent drop. Every part of the line links to the record that proves it. The authority line reads "guaranteed to propose, never apply".

### 6.2 What the product does

Unattended journeys run on their schedules and reach their results without human input: a tracking issue rewritten in place, a proposed change that fixes the defect and passes its checks, or a paced chat post. When a model update, a prompt edit or a GKE change breaks a journey, the next morning's page turns red and the owner receives an issue. A customer can switch models and read the line for the new model.

### 6.3 How we measure

The nightly records every registered test, including on one install where the clock runs unpaused and a chat platform receives posts. Every test declares its skills, its journey and its difficulty level. The shared test system computes the page each morning from the record, per journey, per capability, per skill and per model. A second model runs the same tests as a standing control: a fail on one model with a pass on the other goes to the owner of the check first. A failure of the test infrastructure, such as a rate limit on a lookup, counts as neither a pass nor a fail. Once per release, a bare-model run on the hard levels shows what the product adds.

### 6.4 What the content is

Every audit check cites its source: a published Google guide, a release note, or a named production incident. Every shipped skill is backed by a test or retired. A skill is rules and scripts, with step-by-step prose only where a supported model is proved to need it. Unattended journeys cover real customer failure modes at levels 2 and 3, not only single planted defects. An external benchmark built from public exam tasks, filtered to GKE, compares the product against a bare model with the same cluster tools.

### 6.5 What the team does

Every change to agent behaviour lands with a failing test first and three passes in a row after the fix. Owners review drops every week. Three counters are reported every week: journeys graded and certified, capabilities measured, and proposed fixes merged.

Once a month, the team takes the support-case and post-mortem patterns of the last 60 days, with no customer identifiers, and sorts each pattern into one of five classes: not covered, covered but did not fire, caught but with the wrong fix, knowledge missing, or out of scope. Each class has one outcome: a new check or journey backed by a level 2 or 3 test; a failing test followed by a fix; a test on the proposed change followed by a fix; a catalogue entry with its source; or a recorded reason. The monthly report states what share of the patterns a graded journey now covers. Until a data agreement exists, the loop runs on public GKE known issues, release notes, customer epics and the ledgers of installs that consent.

## 7. The plan

### 7.1 Phases

| Phase                                | Dates                                     | What lands                                                                                                                                                          | Counter it moves                             |
| :----------------------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------- |
| 0. Measurement                       | 10-26 to 11-02                            | Fix the broken checks; tag each test with its skills; add the journey list and the rating calculation to the shared test system; enable Claude on a test project    | Skills measured: 1                           |
| 1. First-run audits                  | Code this week; first nightly about 11-09 | Grade the five first-run audits on their real results inside the existing nightly, with no extra runs                                                               | Unattended journeys graded: 5                |
| 2. Chat evidence and cost            | 11-09 to 11-30                            | An install with a running clock and a chat platform, to grade the stall watch, the event triage and the five paused audits; token, time and route-stability columns | Unattended graded: 5 to 12; measured: 0 to 2 |
| 3. Reliability and the customer view | 11-16 to 12-14                            | Fix the known behaviour defects on Claude; run the tests with skills switched off; show the loaded text versions on the install; ship the page                      | Skills measured: 2 to 4                      |
| 4. Certification                     | After 12-14                               | A private test project and test set; audit-log sweeps; an outside reviewer                                                                                          | The first certified line                     |

Engineering cost: about one person-week for phase 0, days for phase 1, about two person-weeks for phase 2, plus the skill owners' repair loops in phase 3.

### 7.2 Why only 0 to 2 measured unattended journeys by 12-14

Two reasons. First, the pass rates: the compliance audit end to end passes 0.21 on Claude, and the fleet audit skill passes 15 of 23. Even a journey that truly passes 93 percent of the time clears 57 of 60 on a given window only about four times in ten. Second, churn: the skill text changed on 23 of the last 30 days, and every edit restarts the 60-run window. Decision 5 below chooses how the window survives an edit that changes no behaviour.

### 7.3 Risks

| Risk                                             | Evidence                                                                                                | Effect on the plan                                                        |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------ |
| The audits pass well under the bar               | The compliance audit end to end passes 0.21 on Claude; the fleet audit skill passes 15 of 23            | Journeys graded by 11-09; 0 to 2 at the measured bar by 12-14             |
| The rated text changes almost daily              | Skills changed on 23 of 30 days; the fleet audit skill on 22; the five first-run procedures on 10 to 12 | Decision 5 chooses a window key, or the audits never reach the bar        |
| Chat results cannot be graded in the test system | No test install has a chat platform                                                                     | Phase 2 needs a new install or a leased project                           |
| The nightly time budget                          | About 100 tests fit in one job; the split bought 40 to 70 tests of headroom, once                       | Each new test needs a third job or a retired test                         |
| The model walks past a written rule              | Four of the twelve low-scoring tests are the agent against a stated rule                                | Where the route matters, a tool or a check enforces it                    |
| A confident wrong answer on a hard problem       | The record has almost no level 2 or 3 tests                                                             | Every line names its level                                                |
| The scheduler component is due for replacement   | The clock, the pause script and the persona text live in it                                             | Results graded on external artifacts survive; the persona lines move once |

### 7.4 Decisions parked until this concept is agreed

1. What evidence the word "certified" requires.
2. How we trigger and count unattended runs: the three nightly triggered runs under the standard window, with a separate line that shows the real clock fired.
3. How we grade chat results and the five paused audits: a fourth test install with a chat platform and a running clock.
4. What the page shows for the installer's default model (Gemini Flash): "untested" until that model has a nightly of its own.
5. How the window survives a text edit that changes no behaviour.

The options and the recommended answers are in the technical plan, section 14.

## 8. Questions leadership will ask

| Question                                                                | Honest answer today                                                                                                                                                                              | What changes it                                                                                              |
| :---------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| After a month, what can a customer verify that they could not before?   | One line: version control on Claude, 57 of 57 since 10-25. No unattended journey line yet.                                                                                                       | Phase 1 (about 11-09); phase 3 shows the loaded text versions on the install                                 |
| Do the skills add value on a strong model?                              | Unproven for the prose: pass rates with the skill opened and unopened are equal, and 80 of 179 version-control runs used the script without reading the text. Rules and scripts carry the value. | Phase 3 runs the tests with skills switched off; skills shrink to rules and scripts where prose adds nothing |
| Why trust tests you wrote and graded yourselves?                        | Do not call them certified. We plant the defects and write the checks; a model switch exposed eight brittle checks in one week.                                                                  | Step 2 is "measured"; "certified" waits for the private set and the outside reviewer                         |
| Your nightly lost three nights of records. Is the measurement reliable? | The three unsplit nights recorded 22, 0 and 26 of 159 tests. The split nightly recorded 158 of 159 on 10-27.                                                                                     | Three full nights in a row close the item                                                                    |
| What does it cost per night, per journey, per customer?                 | Minutes and tens of thousands of tokens per run, recorded but not yet shown.                                                                                                                     | Phase 2 adds the columns and a per-model formula; never a certified dollar figure                            |
| Which model are you certifying, and is it the default one?              | The nightly rates Claude Opus 5.5. The installer default is Gemini Flash and will show "untested". Our development projects cannot serve Claude today.                                           | Phase 0 access; decision 4                                                                                   |
| How many of the 47 journeys work unattended end to end?                 | 17 are built to; 5 have their start graded; 0 have their result graded; 20 promises have no test.                                                                                                | Phases 1 and 2; unverified claims are tested or removed                                                      |
| What stops the agent from breaking production at 3 a.m.?                | Read-only access rights and a gateway that blocks writes; any forbidden action fails the run.                                                                                                    | Phase 4 adds audit-log sweeps across every run                                                               |
| How is this different from a model vendor's benchmark page?             | Vendors score public prompts once per release. We grade fleet journeys every night on the shipped text and drop the rating when the model or the text drifts.                                    | Phase 0 page; phase 3 view on the install                                                                    |
| What if the customer's outage is not one you planted?                   | Today the tests are self-authored, apart from the retail epic.                                                                                                                                   | Level 2 and 3 tests from the epic; the monthly intake loop                                                   |
| Does the agent follow the same route every night, or get lucky?         | Not compared across runs today; we check that the required scripts ran.                                                                                                                          | Phase 2 route-stability bounds                                                                               |
| Does this survive the scheduler replacement?                            | Yes. Journeys are graded on external results (the tracking issue, the proposed change, the chat post), never on the scheduler's internal state.                                                  | The rule in section 4.1                                                                                      |

## Appendix. Sources

- The journeys, with evidence per row: [`certified-journeys-inventory.md`](certified-journeys-inventory.md).
- The fourteen steps, the tables, the decision options and the review records: [`certified-journeys-technical-plan.md`](certified-journeys-technical-plan.md).
- The counters: the local scorecard of 2026-10-27 and the nightly build logs of 10-23 to 10-27.
