# Certified journeys and capabilities: metrics, evidence bar, and roadmap

Status: design, draft 5, 2026-10-27. Work in progress on a branch. Nothing in this document is built. Tracking issue:
[#3978](https://github.com/gke-labs/kube-agents/issues/3978). Review records and provenance notes:
[`certified-journeys-review-record.md`](certified-journeys-review-record.md). Journey inventory:
[`certified-journeys-inventory.md`](certified-journeys-inventory.md).

## 1. Purpose and scope

This document defines two product metrics and the evidence behind them. It defines the words that the product uses
for a promise. It gives the plan that makes the metrics true, with owners and dates.

The document covers: unattended journeys, capabilities, skills, the nightly measurement system, and the customer
view of the results. It does not cover: the agent runtime, the chat platforms, or the installer.

## 2. Summary

### 2.1 The end state

- A customer reads one line per journey and per model on their own install. The line shows the promise level, the
  pass rate with its bound, the window dates, the text digest that the pod loaded, the difficulty tier, the typical
  run cost, the skills that the runs read, and the last lapse. Each clause links to the record.
- The unattended journeys run on their schedule and reach their outcome with no person. The outcome is a ledger, a
  pull request, or a chat message. Each journey has a route envelope that the record has seen.
- The nightly records every registered case every night. The scorecard is computed in CI. A model update or a text
  change that breaks a journey shows as a red the next morning and opens an issue to the owner.
- Every audit check has a source. Every shipped skill has a case or is removed. Skills are rules and scripts. Prose
  stays only where a supported model needs it.
- The team lands each behaviour change with one red run and three green runs. The team reports three counters each
  week.

### 2.2 The counters

| Counter                                                         | Today (2026-10-27)    | Target 2026-12-14 |
| --------------------------------------------------------------- | --------------------- | ----------------- |
| Skills and capabilities at the eval-tested bar, Claude Opus 5.5 | 1 of 21 tagged skills | 2 to 4            |
| Journeys graded as scheduled outcomes                           | 0 of 17               | 5 to 12           |
| Journeys at the eval-tested bar                                 | 0                     | 0 to 2            |
| Attested lines                                                  | 0                     | 0                 |

### 2.3 The decisions

Five decisions are open and parked (section 9). Three gates start work: the go on the `skills:` key pull request,
the go on the case fix and the nine owner reports, and a Claude-served install.

## 3. Terms

| Term               | Definition                                                                                                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Journey            | A customer outcome from a trigger. Example: a critical over-grant exists; by morning the agent has found it and opened the pull request. A journey is a set of tasks and the path that runs them. |
| Capability         | One operator task with a fixture and a deterministic check. One bench case.                                                                                                                       |
| Skill              | A directory under `agents/<persona>/skills/`. It holds rules, scripts, and prose.                                                                                                                 |
| Employee           | An agent role on a model. Example: the Platform Agent on Claude Opus 5.5.                                                                                                                         |
| Unattended journey | A journey with a trigger that needs no person, no human step before the outcome, and an outcome that the product exports. Also written HOOTL, human out of the loop.                              |
| Run                | One execution of one case. The nightly runs each case three times.                                                                                                                                |
| Window             | The newest 60 runs of one journey, capability, or skill on one model and one text digest.                                                                                                         |
| Eval-tested        | The window passes with a 95% lower bound of 0.85 or more. Rule D1. At least 24 of 24 while the window fills.                                                                                      |
| Lapsed             | The lower bound is below 0.70 on two nightly checks in a row.                                                                                                                                     |
| Attested           | Eval-tested, plus a private set, plus no forbidden action in the window, plus the model named, plus a reviewer outside the team who re-derives the number.                                        |
| Tier               | The difficulty of a case: T1 one planted defect; T2 judgment with a misleading signal; T3 scale, a causal chain, a long horizon, or catalogue knowledge.                                          |
| Lane               | One nightly job. Today: main, main-b, writers, gitlab.                                                                                                                                            |
| Record             | The nightly's case files and run files in the evals bucket, and the dashboard data file.                                                                                                          |

## 4. The problem

The product claims journeys that nobody measures as outcomes. The numbers on 2026-10-27:

| Fact                                                                         | Number                                                                    | Source                                                            |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Journeys claimed or tested                                                   | 47                                                                        | inventory                                                         |
| Journeys with a trigger that needs no person and an agent that does the work | 17                                                                        | inventory; 11 of 22 scheduled jobs are scripts with no model call |
| Of the 17, graded in part by bench cases                                     | 14                                                                        | inventory                                                         |
| Of the 17, graded as a scheduled outcome                                     | 0                                                                         | no check reads a scheduled run's ledger or chat post              |
| Scheduled starts graded                                                      | 5 audits, by one case                                                     | `oobe-first-run-audits`                                           |
| Documented promises with no test and no case                                 | 20                                                                        | inventory, section 4                                              |
| Bench cases on `main`                                                        | 230; 166 registered; 159 scheduled each night; 129 with a planted fixture | `bench/tasks`, `hack/eval/*.txt`                                  |
| Skills at the eval-tested bar on Claude                                      | 1 of 21 tagged (version-control, 57 of 57)                                | local scorecard                                                   |
| Shipped skills that no case names                                            | 23 of 53                                                                  | local scorecard                                                   |
| Nightly cases recorded on the last four nights                               | 22, 0, 26, 158                                                            | build logs; the split job ran first on 2026-10-27                 |

Four causes sit behind these numbers:

1. The nightly pauses the clock-started audits during its lease, except the five first-run audits. No check reads
   the ledger of a scheduled run.
2. No CI install has a chat platform. Chat posts cannot be graded in CI.
3. The nightly was past its budget. About 100 cases fit in 12 hours at parallelism 6 before the split.
4. The checks were validated on one model. Eight checks broke when the nightly moved to Claude.

## 5. Goals and non-goals

Goals:

1. Count unattended journeys with a definition that a customer can check on their own install.
2. Rate capabilities and skills with one rule, per model and per text digest.
3. Give the word "certified" one meaning, or replace it.
4. Make every claim in the customer story true on the record, or date it.

Non-goals:

1. A guarantee of an outcome. A model is probabilistic. The product guarantees authority, not results.
2. A dollar cost on a line. The price depends on the customer's model and provider.
3. One route for every run. Two valid routes to the same ledger are acceptable.

## 6. Design

### 6.1 Promise levels

A promise has one of three strengths. The word follows the strength.

| Level         | What it covers                                                                                                                     | Strength                                              | Word                                                                                               |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Guarantee     | The authority limit: a read-only identity, a proxy that refuses each write verb, each change as a pull request that a human merges | Hard. Enforced outside the model. Tested on each run. | guaranteed                                                                                         |
| Measured rate | The outcome on a journey or capability: the window's lower bound on a named model and text, re-measured each night, with a lapse   | Statistical. A rate with a bound and a date.          | measured; public word today: eval-tested                                                           |
| Attestation   | That the rate was produced as stated: a private set, no forbidden action, the model named, an outside reviewer                     | As strong as the reviewer's independence              | attested; "certified" only if the programme keeps that word, with its definition printed beside it |

The authority line has two parts. Enforced: RBAC read-only, IAM read-only, the proxy refuses the GitHub write verbs.
Observed: zero forbidden actions in the N runs of the window.

Scope: journeys and capabilities can reach the attested level. Skills are rated and not attested. A journey's line
covers the skills that its runs read. A capability or journey is attested with or without a skill. The line states
"skills read: none" when the runs read no skill.

### 6.2 Metric 1: unattended journeys

A journey counts as unattended when three conditions hold:

1. A schedule, a cluster event, or a standing instruction starts it. A chat question does not.
2. No person acts before the outcome. A pull request that a human merges is the agent's outcome; the merge is not.
3. A deterministic check reads evidence that the product exports: the ledger issue, the pull request diff against the
   planted defect, or the chat post. A row in the runtime's own database does not count.

Counting method: a case starts the audit through the product's own trigger path, the path that the first-run stage
uses, three times a night. The usual window applies. One liveness line per audit checks that the real clock fires.
The stronger form, one observation a night from the real clock on an install where nothing pauses it, is a later
option (section 9, decision 2).

Reported as: journeys graded, journeys eval-tested, journeys attested, each out of 17.

### 6.3 Metric 2: capabilities and skills at the bar

Rule D1, decided 2026-10-19 and amended 2026-10-20:

| Part        | Rule                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------- |
| Key         | The skill text digest, the SOP digest, the served model, the mode, and the digest of each declared case |
| Window      | The newest 60 runs on that key                                                                          |
| Eval-tested | Wilson 95% lower bound of 0.85 or more. 24 of 24 while the window fills. 57 of 60 when full.            |
| Lapsed      | Lower bound below 0.70 on two nightly checks in a row                                                   |
| Use floor   | A case counts for a skill only when the model opened the skill in 20% or more of the case's runs        |

Known limit: skills changed on 23 of the last 30 days; fleet-audit on 22. A 60-run window on an exact digest does not
fill for the audits. Decision 5 (section 9) selects the window key.

Reported as: skills and capabilities eval-tested, per model, with the date and the digest.

### 6.4 Baselines

A pass or fail is measured against an answer key. The answer keys today and the ones the plan adds:

| Judgement                     | Answer key                                                                                                  | Today                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Pass or fail                  | The planted defect on the seeded fleet. The check asks if the output names it and nothing it must not.      | Yes: 129 planted cases                     |
| Authority                     | Zero forbidden actions                                                                                      | Yes: gate rung 1                           |
| Judged score                  | The case's own score on `main` at the same key                                                              | Yes                                        |
| Rating                        | The fixed bar of D1                                                                                         | Yes, locally                               |
| The skill against no skill    | The same model with the skill disabled through the product setting (C5)                                     | No                                         |
| One model against another     | The same cases on a second model                                                                            | Partly: Gemini 3.1 Pro, 29 nights to 10-19 |
| The agent against an operator | One SRE runs the journey by hand once                                                                       | No                                         |
| Real customer failures        | Support patterns triaged into cases (section 6.9)                                                           | No                                         |
| An external syllabus          | Capability tasks in the shape of the CKA exam tasks, filtered to GKE, with the bare model as the second arm | No; parked                                 |

Difficulty tiers: each case gets a tier label, T1, T2, or T3. Today the record is almost all T1. A line names its tier.
The bare-model arm runs on T2 and T3 first, because that is where a gap would show.

### 6.5 Secondary measures

| Measure              | Recorded today                                                                                           | In the rating | Proposed                                                                                                                                                                             |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Latency              | Yes, per run                                                                                             | No            | Reported on the line: median and p90. Lapse flag at 1.5 times the value at certification, two checks in a row. Not blocking.                                                         |
| Tokens               | Yes, per run; not in the dashboard record                                                                | No            | Written into the record. Reported: median total and cached share. Same lapse flag.                                                                                                   |
| Cost in money        | No                                                                                                       | No            | Reported as tokens with a per-model price note. Never certified.                                                                                                                     |
| Trajectory stability | No. The route is recorded; route checks exist per case; nothing compares one night's route with the next | No            | Per journey and model: tool-set overlap (median 0.8 or more), step spread (p90 over median 2.0 or less), zero loops, cost spread 1.5 or less, and envelope drift as an early warning |
| Effectiveness        | No                                                                                                       | No            | Pull requests accepted and pull request quality per journey; findings acted on from the queue; time to first finding; incidents found before a person; the baselines above           |

The one effectiveness number today: on the maintainers' own install, the audits opened 18 remediation pull requests
in 30 days; 0 were merged.

### 6.6 Skills

A skill has three parts:

| Part    | Role                                                           | Value on a strong model                                                                    | Policy                                                             |
| ------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Rules   | House decisions: severity grades, declared intent, skew policy | High. The model does not invent them the same way each run.                                | Keep. Source each rule (section 6.8).                              |
| Scripts | Deterministic collectors and verbs                             | High. 80 of 179 version-control uses ran `vcs.py` with no text read.                       | Keep.                                                              |
| Prose   | The route for a model that needs it                            | Low on Claude: pass rates with the skill open and closed are equal on each comparable case | Keep only where the no-skill arm shows a supported model needs it. |

A skill is rated, not attested. The rating is the repair signal. Each text edit restarts the skill's window. The
per-skill plan is in section 7, step 10.

### 6.7 The measurement system

| Component                  | Today                                                          | End state                                                                                                      |
| -------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Lanes                      | main and main-b (split live since 2026-10-27), writers, gitlab | Plus one install where the clock runs unpaused and a chat platform receives posts                              |
| Record key                 | `setup_id` only                                                | Skill digest, SOP digest, model, mode, case digest                                                             |
| Journey entity             | None                                                           | `docs/designs/journeys.yaml`: one entry per journey with trigger, outcome, owner, tier, and case ids           |
| Rating calculation         | A script on one laptop, each morning                           | `ratings.py` in CI over the dashboard data file; a generated scorecard region                                  |
| Lapse path                 | Issues only for three-night 0-of-3 reds                        | An issue to the owner when a journey or skill sits below 0.70 on two checks                                    |
| Infrastructure versus fail | Per case rules                                                 | A GitHub 429 on a ledger lookup is infrastructure, not a fail                                                  |
| Customer view              | None                                                           | The pod reports its loaded digests; a scorecard page on the install matches the record to them                 |
| Second-model control       | Not a rule                                                     | A second model runs the same cases; a red on one model with a green on the other goes to the check owner first |

### 6.8 Content provenance

The audit checks are the maintainers' practice. Today: 14 of 15 governance SOPs cite no Google document. The readiness
skill's catalogues cite Google pages (34 links in the known-issues list; 6 of 24 rule modules). The 31 mirrored Google
skills are Google's own text with patches on 26.

Rule: each check gets a `source:` line, a Google guide, a release note, or a named incident. A check with no source is
labelled "maintainers' practice" and reviewed. Each audit gets a coverage map against its benchmark: items checked as
posture, items checked as drift, items missing with a reason, and items beyond the benchmark. The compliance audit's
map is the template: 12 of its 17 checks map to the CIS GKE Benchmark, the Pod Security Standards, or the GKE
hardening guide; 5 are operational checks from experience. The full map is in the review record.

### 6.9 The intake loop

Monthly, over the trailing 60 days of support cases and postmortems, with an approved anonymised export:

1. Intake: patterns with category, symptom, root cause, time to detect, time to fix, and the GKE version.
2. Triage: score each pattern on frequency, severity, whether a scheduled check could see it before the incident, and
   whether the fix is a declarative change. Assign a gap type: not covered, covered but did not fire, caught but wrong
   fix, knowledge missing, out of scope.
3. Fixture: plant the pattern on the seeded fleet or a prebuilt stack.
4. Case before change: the case runs red on `main`; the skill, SOP, or catalogue change lands with three greens.
5. Report: the share of the period's patterns covered by a graded journey, by gap type.

Prerequisite: a data agreement for support cases. Until then the loop runs on the public known-issues page, the release
notes, and the customer epic [#2597](https://github.com/gke-labs/kube-agents/issues/2597).

## 7. Plan

Weeks are ISO weeks of 2026. W44 is 10-26 to 11-01. A pull request that grows past twice its size stops and asks.

| #   | Step                                             | What is built                                                                                                                                                                                                                                                     | Owner                                                          | Starts                                   | Done when                                                            | First result                               | Week                               |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------ | ---------------------------------- |
| 0   | Gates                                            | Three gates: the go on the `skills:` key PR; the go on the case fix and nine owner reports; a Claude-served install (Model Garden on one dev project, or a leased CI pool project)                                                                                | project lead                                                   | now                                      | each gate answered                                                   | none                                       | W44                                |
| 1   | A whole nightly record                           | The split job (live 10-27), per-repetition recording, the slow tail found                                                                                                                                                                                         | eval crew                                                      | in flight                                | three nights in a row record every case                              | 158 of 159 on 10-27                        | W44 to W45                         |
| 2   | Measurement on `main`                            | 2a `skills:` key and validator, 126 lines; 2b `journeys.yaml` and validator, 100 lines; 2c tokens in the record, 30 lines; 2d `ratings.py`, 300 lines plus tests; 2e generated scorecard region, 100 lines; 2f lapse filer, 60 lines; 2g retire the laptop script | the author                                                     | 2a on its gate; 2b to 2g queued for a go | CI produces the scorecard each morning                               | first CI scorecard                         | 2a W44; 2b to 2d W45; 2e to 2g W46 |
| 3   | Scheduled outcomes graded                        | A `lookup:` field on `ledger_issue_contains` (label plus since-time, 40 to 60 lines); five outcome checks on `oobe-first-run-audits`, each with its silence half; the retrospective's outcome asserted as silence; a 429 is infrastructure                        | the author; case owner by report                               | after 2b                                 | five checks pass where the ledger exists and fail where it does not  | five audit outcomes nightly, about 11-09   | W45 to W46                         |
| 4   | The twelve measurement defects                   | `after_result_pattern` on `obtainability-design-quota-vs-capacity`, 12 lines, under [#3128](https://github.com/gke-labs/kube-agents/issues/3128); a question on [#2344](https://github.com/gke-labs/kube-agents/issues/2344); nine comments on the owners' issues | the author; owners                                             | on its gate                              | the case reads the typed command; nine issues have an owner's answer | that case from 1 of 9 to 9 of 9            | W44 to W45                         |
| 5   | An install where the clock runs and chat is read | A decision memo; then one pool project with a chat app, audits unpaused, no GitHub-writing cases beside them, a Prow periodic; outcome checks for the stall watch, the event triage, and the five paused audits                                                   | eval crew; the author                                          | after the memo                           | stall watch and event triage report nightly                          | journeys graded from 5 to 10 or more       | memo W46; job W47 to W48           |
| 6   | Two behaviour fixes                              | A persona line for the forge-CLI miss; a persona line for the dismissal. Each: red on `main`, three greens on a Claude-served install                                                                                                                             | skill owners                                                   | on the Claude gate                       | three greens, registered                                             | two cases from 7 of 9 and 0 of 9 to 9 of 9 | W46 to W47                         |
| 7   | The hard tier                                    | Tier labels in `journeys.yaml`; 10 to 15 T2 and T3 cases from the customer epic with fixtures; the fleet sized against the budget                                                                                                                                 | domain owners; the author writes the proposal and two fixtures | after 2b                                 | cases graded nightly with their tier                                 | the first pass rate by tier                | W46 to W49                         |
| 8   | The bare-model arm                               | The skill-disable setting, one `PlatformAgent` field, 150 lines; the arm on version-control and the 13 passing fleet-audit cases, one lease each; then T2 and T3                                                                                                  | operator owner; the author                                     | setting after 2; runs after 6            | headroom per tier published beside the rate                          | helps, equal, or hurts for version-control | setting W47; runs W48 to W49       |
| 9   | Provenance                                       | A `source:` line on every check; a coverage map per audit; a checker for new checks                                                                                                                                                                               | domain owners; the author writes the template                  | now                                      | every check cites or is labelled                                     | the compliance map, 17 checks              | W45 to W49                         |
| 10  | Skills triage                                    | The two-reader tags (PR 2, 450 lines); one decision per untagged skill, 30 of them; shrink to rules and scripts where the arm shows no prose value                                                                                                                | skills-content owner decides; the author prepares              | PR 2 after 2a; decisions after 8         | every shipped skill has a case or is removed                         | skills with no case from 23 of 53 to 0     | PR 2 W46; decisions W49 to W50     |
| 11  | The customer's own view                          | The pod reports loaded digests, 300 lines; the scorecard page on the install                                                                                                                                                                                      | operator owner; the author                                     | after 2d                                 | a customer reads the line and the digest matches                     | the first install with its own line        | W48 to W50                         |
| 12  | The attested step                                | The private set (a pool project, a private repository, a bucket, a seeded fleet); the reviewer procedure; the audit-log sweep, 250 lines                                                                                                                          | eval crew                                                      | after 1, 7, 11                           | one journey carries an attested line                                 | that line                                  | after W50                          |
| 13  | The weekly cadence                               | Three counters from 2d; a weekly note; a lapse review                                                                                                                                                                                                             | the author                                                     | after 2d                                 | four weeks of reports                                                | the first weekly note                      | W46 on                             |
| 14  | The intake loop                                  | The data agreement; the monthly triage note; a proxy run on public sources first                                                                                                                                                                                  | intake owner; domain owners                                    | proxy now; real run on the agreement     | the first monthly coverage report                                    | the proxy report                           | proxy W47                          |

The weeks at a glance:

| Week      | Active steps                           | What exists at the end of the week                                                                                           |
| --------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| W44       | 0, 1, 2a, 4                            | Gates answered; the `skills:` key and the case fix open as pull requests; nine reports posted                                |
| W45       | 1, 2b to 2d, 3, 4, 9                   | The journey entity and tokens in the record; the lookup field and five outcome checks open; the compliance coverage map      |
| W46       | 2e to 2g, 3, 5 memo, 6, 7, 10 PR 2, 13 | The scorecard produced by CI; five audit outcomes nightly; the install memo; the behaviour loops started; the first T2 cases |
| W47       | 5, 6, 7, 8 setting, 9, 14 proxy        | The install job; two persona fixes green; the skill-disable setting open                                                     |
| W48       | 5, 7, 8 runs, 11                       | Chat-evidenced journeys graded; the first bare-model result; loaded digests open                                             |
| W49       | 7, 8, 9, 10                            | Headroom per tier; source lines done; the skills triage table                                                                |
| W50       | 10, 11, 13                             | The customer's own view on one install; triage decisions; four weeks of counters                                             |
| after W50 | 12                                     | The first attested line                                                                                                      |

## 8. Risks and limits

| Risk                                    | Evidence                                                                                           | Effect on the plan                                                               |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| The audits pass well under the bar      | The request-graded compliance audit passes 0.21 on Claude over 34 runs; fleet-audit reads 15 of 23 | Journeys graded by 11-09; journeys eval-tested 0 to 2 by 12-14                   |
| The rated text changes almost daily     | Skills changed on 23 of 30 days; fleet-audit on 22; the five SOPs on 10 to 12                      | Decision 5 selects a window key, or the audits never rate                        |
| Chat evidence is unreadable in CI       | No CI install has a chat platform; the stored-post table fills only with a platform                | Steps 5 and 6 depend on a new install or a leased pool project                   |
| The nightly budget                      | About 100 cases fit per lane; the split buys 40 to 70 cases of headroom once                       | Each new case needs a third lane or a retired case                               |
| The model walks past a prose rule       | Four of the twelve low cases are agent behaviour against a stated rule                             | Where the route matters, a tool or a check enforces it                           |
| A confident wrong answer on a hard case | The record has almost no T2 or T3 cases                                                            | A line names its tier; T1-only lines say so                                      |
| Hermes replacement                      | The scheduler clock, the pause script, and the persona text are Hermes-side                        | The trigger-path method and the ledger evidence survive; persona lines move once |

## 9. Open decisions (parked on 2026-10-26)

Each decision carries a recommendation. None blocks steps 1 to 4.

| #   | Decision                               | Options                                                                                                                                                                                      | Recommendation                                                                                               |
| --- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| 1   | The word for the top level             | a) all four pieces of evidence; b) without the private set; c) keep "eval-tested" only                                                                                                       | a as the definition now; "attested" as the word; size the private set when the first journey reaches the bar |
| 2   | The unit of an unattended journey      | a) one observation a night from the real clock; b) the product's trigger path, three runs a night; c) count starts only                                                                      | b                                                                                                            |
| 3   | Chat evidence and the paused audits    | a) a fourth install with a chat app; b) the five first-run audits only; c) nothing                                                                                                           | b now; a as a phase-2 decision with its cost                                                                 |
| 4   | The line for a default install's model | a) a Gemini Flash lane; b) "untested" with the reason; c) change the installer default                                                                                                       | b now; a when the budget allows                                                                              |
| 5   | The window key                         | a) a freeze on the five SOPs and fleet-audit; b) key on the text and scripts the agent reads and runs, normalised; c) tolerate a digest change when declared cases are unchanged; d) keep D1 | b                                                                                                            |

Also parked: the capability set in the shape of the CKA exam tasks, 20 to 30 tasks, two arms, three runs each.

## 10. Customer positioning

This section is the customer-facing summary. It states only what the record supports.

kube-agents turns a frontier model into an operator that a customer can leave alone on their fleet. It can only
propose. It works before the incident. It does the same thing each night. It shows the record.

Comparison with the alternatives:

| Property                            | A chat model                           | An in-house agent                       | kube-agents                                                                                                                                |
| ----------------------------------- | -------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Starts with no person               | No                                     | Yes, after the team builds the schedule | Yes: 10 audits, a stall watch, event triage, a readiness check, with procedures and delivery written and re-tested each night              |
| Authority limit                     | The credentials that the person pasted | After the team builds and tests it      | Enforced outside the model and tested on each run: read-only identity, a proxy that refuses each write verb, each change as a pull request |
| Regression visible the next morning | No                                     | After the team builds a second product  | Yes, on the exact text that shipped; a regression tripwire and an authority proof; not yet a measure of competence on hard problems        |
| GKE knowledge                       | General                                | Written by the team                     | Executed, perishable, overridable: catalogues of known issues and removed APIs, 117 audit checks, collectors; sources to be added          |
| Kept current; model choice          | One model                              | At the team's pace; usually one model   | Updated with the product; the same journeys on Gemini, Claude, or an OpenAI-compatible model, one line per model                           |

Preventive care, not the emergency room: a chat model answers after a person notices a symptom. kube-agents runs the
check-up on a schedule and names the risk while the fleet is healthy. The record today: 11 of the 17 unattended
journeys are preventive; the emergency-room journeys are the more reliable ones by measurement; 0 of the 18
remediation pull requests on the maintainers' install were merged. The plan starts with the audits for that reason.

Not yet true, with a date: no journey is graded as a scheduled outcome (W46); nothing reaches a customer's own install
before step 11 (W50); the word "certified" waits for step 12.

## Appendix A. Sources

- Journey inventory: [`certified-journeys-inventory.md`](certified-journeys-inventory.md).
- Review records, panel table, and the compliance audit's benchmark map:
  [`certified-journeys-review-record.md`](certified-journeys-review-record.md).
- Rules: `docs/designs/testing-strategy.md` sections 3 and 4; `.agents/rules/eval_driven_development.md`; the gap plan
  decisions D1 to D6 and H (local).
- Numbers: the local scorecard and dashboard of 2026-10-26 and 2026-10-27; the nightly build logs of 2026-10-23 to
  2026-10-27; `git ls-tree` on `upstream/main` for case and skill counts.
