# Certified journeys and capabilities: the metrics, the evidence bar and the engineering roadmap

Status: design draft 4, 2026-10-26. Built on a journey inventory of the same day ([`certified-journeys-inventory.md`](certified-journeys-inventory.md),
47 rows with file:line evidence). Reviews so far: a blind red-team of draft 1 (10 findings, 8 changed the plan), a
chief-of-staff check of draft 3 (10 facts corrected) and an expert panel of five on draft 3 (unanimous concerns, nothing
blocking; five items folded). Records at the end. Work in progress on a branch, not merged; nothing it proposes is built. Tracking issue:
[#3978](https://github.com/gke-labs/kube-agents/issues/3978).

The questions this document answers: which core metrics we track (unattended journeys, certified capabilities), the engineering
roadmap that delivers them, how many journeys can run with no human and which, how many we add a week and how the loop
scales, how a journey or skill is certified, what testing in the loop means here, and what customers want.

## 1. The end state, and the steps to it

### 1.1 The end state

**What a customer sees.** On their own install, a page with one line per journey and per model: the promise kind
(guaranteed, measured, attested), the rate and its bound, the window dates, the exact text digest the pod loaded, the
difficulty tier, the typical run in minutes and tokens, the skills the runs read, and the last lapse. Every clause links
to the record that proves it. The authority line reads "guaranteed to propose, never apply", enforced by IAM and the
proxy and observed as zero forbidden actions in the window.

**What the product does.** The unattended journeys run on their schedule and reach their outcome with nobody typing: a
ledger rewritten in place, a pull request whose diff fixes the defect and passes CI, a paced chat line. Each journey
has a route envelope the record has seen. A model update, a text edit or a GKE change that breaks a journey shows as a
red the next morning and files an issue to the journey's owner. A customer can switch models and read the same line.

**What the measurement system is.** A nightly that records every registered case every night, across its lanes,
including one install where the clock is not paused and a chat platform receives posts. Every case carries its skills,
its journey and its difficulty tier. The scorecard is computed in CI from the nightly record, per journey, capability
and skill, per model, with tokens and latency beside the rate. A bare-model arm runs per release on the hard tier. A
private set the authors never see, and a named reviewer outside the team, back every attested line. A second model runs
the same cases as a standing control for check defects.

**What the content is.** Every audit check carries its source: a Google guide, a release note or a named incident.
Every shipped skill has a case or is retired; skills are rules and scripts, with prose only where a supported model is
shown to need it. The unattended journeys cover the customer epic's problems at tiers 2 and 3, not only planted
defects. A capability set in the shape of the CKA tasks, filtered to GKE, runs against the same two arms.

**What the team does.** Every change to agent behaviour lands with its red and three greens. Lapses are reviewed
weekly with their owners. Three counters are reported weekly: journeys graded and attested, capabilities measured,
pull requests accepted.

### 1.2 The steps, in order

| #   | Step                                                                                                                                                    | Done when                                                                                | Depends on                               | Owner                          |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------ |
| 0   | The decisions: the word and its definition, the unattended-journey unit, the window key, the default install's model line, Claude on one dev project    | Each is answered in [#3978](https://github.com/gke-labs/kube-agents/issues/3978)         | nothing                                  | project lead                   |
| 1   | A whole nightly record: the second half scheduled, cases recorded per repetition, the slow tail found                                                   | Three nights in a row record every registered case                                       | in flight                                | eval crew                      |
| 2   | Measurement on `main`: the `skills:` key, the journey entity, the tier label, tokens in the record, the rating calculation in CI, a generated scorecard | CI produces the scorecard each morning without a laptop                                  | 0                                        | the author                     |
| 3   | Scheduled outcomes graded: the lookup field and five outcome checks on the existing first-run case                                                      | Five audits report an outcome every night                                                | 1, 2                                     | the author                     |
| 4   | The twelve measurement defects: one case fix of ours, nine reports to owners                                                                            | Each low case has an owner's answer; the two display-line cases read the typed command   | 0                                        | the author, owners             |
| 5   | An install where the clock runs and chat is read                                                                                                        | The stall watch and the event triage report outcomes nightly                             | 0 (question 3), eval crew                | eval crew, the author          |
| 6   | The two behaviour fixes on a Claude-served install: the forge-CLI miss, the dismissal                                                                   | Red on `main`, three greens, registered                                                  | 0 (the enable)                           | skill owners                   |
| 7   | The hard tier: ten to fifteen tier 2 and 3 cases from the customer epic, with their fixtures                                                            | Graded nightly with tier labels; the fleet sized against the budget                      | 1, 2                                     | case authors                   |
| 8   | The bare-model arm, per release: the product's disable setting for skills, and the capability set's second arm                                          | Headroom per tier published beside the rate                                              | 6 (the install), 7                       | the author, operator owner     |
| 9   | Provenance: a source line on every audit check                                                                                                          | Every check cites a guide, a release note or an incident, or is labelled and reviewed    | nothing                                  | skill owners                   |
| 10  | Skills triage: tag or retire the untagged thirty; shrink to rules and scripts where the arm shows no prose value                                        | Every shipped skill has a case or is gone                                                | 2, 8                                     | skill owners                   |
| 11  | The customer's own view: the pod reports its loaded digests; the scorecard page on the install                                                          | A customer reads the line on their install and the digest matches                        | 2                                        | operator owner                 |
| 12  | The attested step: the private set, the reviewer, the audit-log sweep across the window                                                                 | One journey carries an attested line                                                     | 1, 7, 11                                 | eval crew                      |
| 13  | The weekly cadence: lapse review, three counters                                                                                                        | Four weeks of reports                                                                    | 2                                        | the author                     |
| 14  | The intake loop: support patterns of the trailing 60 days triaged monthly into journeys, cases and catalogue entries (section 18)                       | The first monthly report shows the share of support patterns covered by a graded journey | a data agreement for support cases; 2, 7 | an intake owner, domain owners |

Steps 0 to 4 are this month. Steps 5 to 8 are November. Steps 9 to 11 run beside them and finish by mid-December.
Step 12 is the first line after 12-14. Section 13 carries the dates and the counter targets; section 14 the open
decisions; the sections between hold the evidence for each step.

### 1.3 Today against the first milestone

| Counter                                                 | Today | 2026-12-14 target | What it depends on                                                                    |
| ------------------------------------------------------- | ----- | ----------------- | ------------------------------------------------------------------------------------- |
| Skills and capabilities at the eval-tested bar (Claude) | 1     | 2 to 4            | a whole nightly record; 8 clean nights per one-case skill                             |
| Journeys graded as scheduled outcomes                   | 0     | 5 to 12           | five checks on an existing case (about 11-09); a chat-capable install for the rest    |
| Journeys at the eval-tested bar                         | 0     | 0 to 2            | the audits pass 0.21 to 0.65 today; the rated text changes 22 of 30 days (decision 5) |
| Certified lines                                         | 0     | 0                 | the private set is not built in this window                                           |

## 2. The story: why a customer runs kube-agents instead of their own agent or a generic LLM

**The story in one sentence.** kube-agents turns a frontier model into an operator you can leave alone on your fleet:
it can only propose, it works before the incident, it does the same thing every night, and it shows you the record.
Each clause is a measure. "Can only propose" is the authority limit, zero forbidden actions in the window. "Before the
incident" is the habit, journeys graded as scheduled outcomes. "The same thing every night" is the variance we remove:
the same fleet, text and model give the same outcome at the stated rate and a route inside a known envelope. "Shows you
the record" is the line per journey and model, with its lapse. Reducing variance is the engineering half of this; the
value half is that the fleet stays out of the emergency room and the fixes arrive as pull requests someone merges.
Neither half is the product without the other: a perfectly repeatable agent that prevents nothing is a metronome, and
a brilliant agent that behaves differently each night cannot be left alone. And not all variance is the enemy: two
valid routes to the same ledger are fine; the variance to remove is in the outcome and the authority, and in a route
that drifts without anyone noticing.

A generic LLM is a chat window: it answers when someone types, with whatever access that person pastes in, and
nobody measures it on your fleet. An agent you build yourself can be made to run on a schedule, but you then own the
identity, the audit trail, the test fleet and the nightly record, and most teams never get past the first two.

kube-agents is the operator you do not have to hire, with the authority you would give a new one. Each of the five
points below can be built in-house; the product is that they exist, work together, and are measured every night:

1. **It ships the operator's calendar and procedures, not a cron slot.** Anyone can schedule an agent. What runs on
   the schedule here is the content: ten fleet audits, each with a written procedure of numbered checks, a flag rule,
   a do-not-flag rule, a severity and a remediation; a readiness pre-flight before upgrades; a stall watch every 30
   minutes; triage on a warning event; a ledger per audit rewritten in place; a pull request per critical fix; and a
   paced chat delivery of two critical items a day. All of it runs before the incident, which is the habit of section
   2.1. An in-house agent starts with an empty calendar and writes this itself; a chat model has no calendar. The value
   is the months of operating procedure already written, wired to delivery, and re-tested every night.
2. **Its authority limit is enforced outside the model and tested every night.** Read-only IAM is easy to grant; the
   value is the rest: a credential proxy that refuses every merge, approve and mutating API call whatever the prompt
   says, a pull-request-only write path with fast-forward rules, one Cluster Agent per cluster pinned to its own
   kubeconfig, and a gate in which any forbidden action fails the run. An in-house agent gets this boundary when
   someone builds and tests it; a chat session has whatever credentials the person pasted. The worst case here is a
   wrong pull request, never a wrong change.
3. **It cannot regress silently.** Every night, the exact text that shipped runs 159 cases on the same seeded fleet,
   three times each, and any forbidden action fails the run. Be precise about what that measures today: the defects
   are planted and mostly simple, so the record is a regression tripwire and an authority proof, not yet a measure of
   competence on hard problems (section 17 is that). A tripwire does not need hard cases; it needs the same cases every
   night, so a model update, a text edit or a GKE change that breaks a journey shows as a red the next morning instead
   of in a customer's fleet. The line a customer reads is per journey and per model ("version-control on Claude Opus
   5.5: 42 of 42 since 10-25" is the one that exists), it starts a new window when the text changes, and it lapses when
   the rate falls. An in-house agent has no tripwire unless the team builds a second product; a model vendor's
   benchmark does not re-run your journeys when the model changes. The competence claim is earned later, by the hard
   tier and the bare-model arm; the no-silent-regression claim is the one the record supports now, and the last three
   nights (22, 0 and 26 cases recorded) show it only holds when the record is whole.
4. **It executes GKE guidance that is perishable, tested and overridable, and lets you add your own.** A customer
   can write best practices; most teams have a wiki of them that nothing runs. What is hard to write and harder to
   keep is the GKE-specific, perishable part: which minor versions each channel serves this month, the 52 removed APIs,
   the 33 known issues with their affected versions, the skew policy, the capacity and calendar-mode APIs, what the
   upgrade will refuse. Here each practice is a check that runs: a flag rule, a do-not-flag rule, a severity, a
   remediation and a planted case that proves it still works, 117 checks across 10 domains, 24 readiness rule
   modules, collectors that read the whole fleet in one pass. A declared posture overrides any check without an
   argument, so a customer's own rule wins where they have one, and an operator's own scheduled checks run beside ours.
   Two honest limits decide how much this is worth. The record says the rules and the scripts are what the model does
   not invent on its own, while how-to prose adds little on a strong model, so the value sits in the lists and the
   collectors, not in the text. And "it follows Google's published GKE guidance" is true only in parts today, measured on `main`: the 31 mirrored
   Google skills are Google's own text with our patches on 26; the readiness skill's catalogues trace to Google pages
   (34 links in the known-issues list, citations in 6 of the 24 rule modules and in the removed-API scan); but 14 of the
   15 audit procedures cite no Google document, and the one SOP with reference lines points at our own mirrored skill
   files. The 117 audit checks are the maintainers' practice. The plan (section 16, step 8) gives every check a source
   line, a Google guide, a release note or a named incident, and labels or retires the ones that have none; a customer
   should want Google's published guidance for Google's product executed and kept current, not another team's opinions.
5. **It is kept current, and it is not married to one model.** GKE changes every month: channel defaults, removed APIs,
   new known issues, new capacity APIs. The catalogues and procedures are updated with the product and the nightly
   re-tests them against the same planted fleet, so a change that breaks a journey shows as a red the next morning.
   The same journeys run on Gemini, Claude or an OpenAI-compatible model, and the line is per model, so a customer can
   switch models and read the same line for the new one. An in-house agent rots at the pace of the team that owns it
   and is usually bound to the model it was built on; a chat model is one model.

It runs in your project, on your model and your billing, with telemetry in your project and prompts going only to
your provider (`reference/security-and-iam.md`, "What leaves for the model provider"); that is table stakes against an

**The reputational reason, stated plainly.** Part of why a customer wants the vendor's guidance for the vendor's
product is cover, not insight: a platform lead who followed Google's published GKE guidance, executed by a tool from a
Google team, has an answer when something goes wrong that a home-grown checklist does not give; the posture is one
Google support will recognise, and a security review accepts a known name faster than an internal script. That reason
is real for the person who carries the risk, and it cuts both ways. It exists only if the checks trace to published
guidance and meet the brand's quality bar: a check labelled "recommended" that is wrong costs the brand more than a
missing check, which is why provenance (section 16, step 8) and the certified ladder matter more here than for a
neutral tool. And it is weaker while the product carries a "labs" name: the cover a customer gets is the cover the name
gives. The design treats this as a reason to earn the brand's bar, not as a value to claim before it is met.
in-house build and is stated here so nobody has to ask.

What is true today, and what is a promise with a date: one skill is at the bar on Claude (version-control, 42 of 42);
no journey is yet graded end to end as a scheduled outcome; nothing of this reaches a customer's own install until the
pod reports the digests it loaded (phase 3). The roadmap in section 13 grades the five first-run audits as scheduled
outcomes from their first nightly, about 11-09, and uses the word "certified" only when a reviewer outside the team
can check the claim from the record.

### 2.1 Healthy habits, not the emergency room

A model you ask when something is broken is the emergency room: good at the visit, silent until the ambulance. Your own
chat session, and an agent you built to answer questions, both work this way; they start when a person notices a
symptom, which is after the outage has begun. kube-agents is meant to be the healthy habit: the checks and the hygiene
that keep the fleet out of the emergency room, run on a schedule while nothing is wrong, so the budget that would block
a drain, the pool pinned to one zone, the binding that grants too much and the control plane one minor behind are named
before the upgrade, the stockout or the audit that would have found them.

What makes it a habit rather than a slogan, in the product today:

| Habit                              | What runs, and when                                                                                                                                                                                                               | Where it comes from                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| The scheduled check-ups            | Ten audits on a cron: compliance and reliability daily, cost, drift and patch readiness weekly, AI security, stockout, networking and GCE daily, the upgrade retrospective on Sundays; the first five also run once at onboarding | `agents/platform/cron/jobs.json`                  |
| The pre-flight before a change     | Upgrade readiness graded per cluster before anyone schedules the upgrade: drain-blocking budgets, fail-closed webhooks, exclusions, version skew, 24 rule modules, 33 known GKE issues, 52 removed APIs                           | the fleet-upgrade-verification skill              |
| The written standard of care       | 15 governance SOPs, 10 of them with 117 numbered checks, each with a flag rule, a do-not-flag rule, a severity and a remediation; 26 of the 31 mirrored Google skills patched for production use                                  | `agents/platform/governance/`, the skill overlays |
| Respect for a declared choice      | A posture the repository declares on purpose is listed as declared intent, not raised as a finding, so the habit does not nag                                                                                                     | the declared-intent rules in every audit SOP      |
| A paced regimen, not alarm fatigue | At most two critical items a day and three non-critical after 16:00, and no new items while one waits for a decision                                                                                                              | the findings nudge                                |

**Where the product is on this scale today.** By design and by volume it is a habit product: 11 of the 17 unattended
journeys look for latent risk before anything fails (the ten audits and the weekly readiness brief), and about 96 of
the registered cases grade preventive domains (upgrades 49, security 10, reliability 11, fleet audits 12, capacity 6,
cost 4, consistency 4) against about 23 that grade the emergency room (incident triage 13, cluster debugging 10). By
measured maturity the order is reversed: the emergency-room journeys are the reliable ones (the crashloop debugging
cases block the presubmit and pass; the event triage passes), while the preventive audits carry most of the known
defects (fleet-audit reads 15 of 23 on Claude, and seven of the eight cases that fail every run are audits). And the
habit's output is not yet acted on: on the maintainers' own install, 0 of the 18 remediation pull requests the audits
opened in 30 days were merged. So the honest sentence is: kube-agents promotes the habit, measures the emergency room,
and has not yet shown that anyone keeps the habit. The roadmap's first journeys are the audits for that reason.

Two honest limits. The standard of care is the maintainers' practice, not a published standard; no check cites a Google
document yet, and section 6 says how an outside syllabus could change that. And the habit is only worth what the record
shows: a scheduled check that nobody measures is a promise, which is why section 9 counts outcomes graded, not jobs
scheduled.

The analogy is still open. "Healthy eating" is the plainer phrase. The aviation frame maps every part (pre-flight
checklist, maintenance interval, airworthiness directives for the known issues, an approved work order for every change)
and gives the word "certified" its exact meaning: an inspector outside the crew signs against a standard. Whichever is
chosen, the sentence a customer should remember is the same: the agent is there to keep you out of the emergency room,
and it keeps a record that shows whether it did.

## 3. What "certified" means (proposal, not decided)

The word is a ladder of claims. Each step adds one piece of evidence a customer can check without trusting us. A
claim sits on the highest step whose evidence exists; the word "certified" is the top step only.

| Step | Word                           | What must be true                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Who can check it                                              | Today                             |
| ---- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------- |
| 0    | Claimed                        | The docs say the agent does it.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Nobody.                                                       | 20 promises sit here              |
| 1    | Tested                         | At least one case or journey test exists, runs in the nightly, and has passed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Anyone with the nightly record.                               | most journeys and skills          |
| 2    | Eval-tested (today's "Rated")  | The newest 60 nightly runs on one model, on the exact text and scripts, pass with a 95% lower bound of 0.85 or more (D1). Lapses below 0.70.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Anyone with the record and the digest.                        | 1 skill (version-control, Claude) |
| 3    | **Certified**                  | Eval-tested, **and** all of: (a) a **private set**: cases the skill or journey author never saw, owned by the eval crew, passed on the same window rule; (b) **authority**, stated two ways: _enforced_ (RBAC read-only, IAM read-only, the proxy refuses the GitHub write verbs) and _observed_ (0 forbidden actions in the N runs of the window, the C6 audit-log sweep); (c) **the model named**: the claim carries the model and the digest, and a default install's model shows its own line or "untested"; (d) **reproducible**: an independent reviewer, not the author, re-derives the number from the published record, and the record shows the agent took a stable route to it (the trajectory envelope, section 5.1). | A reviewer outside the authoring team, from the record alone. | 0                                 |
| 3+   | Certified, with measured value | Step 3 plus the no-skill arm (C5): the same cases with the skill removed, so the line can say "helps", "equal" or "hurts".                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Same.                                                         | 0                                 |

What a customer reads: one line per journey or skill and per model, for example "Certified: compliance audit on Claude
Opus 5.5, since 2026-11-20, 60 of 60 on text a1b2c3, private-set 24 of 24, no forbidden action in 60 runs, reviewed
by <name>". Every clause links to the record that proves it.

Scope, one sentence: **journeys and capabilities (a bench case each) can be certified; skills are rated.** A journey is an outcome a customer buys
(the compliance audit finds the over-grant and opens the PR); a task is one capability ("grade upgrade readiness");
a skill is a file, and its rating is derived from the tasks that use it. The independent reviewer of step 3d is a named
member of the eval crew who did not write the skill or the case, and the name goes on the line.

**A capability or journey is certified with or without a skill.** The claim is about the agent as deployed on a named
model: the identity and its limits, the tools, the schedule, the record, and whatever skill text the run chose to read.
A strong model passes many cases without opening any skill (on Claude, 9 of 11 Cluster Agent cases never open theirs
and pass), and that pass is as real to the customer as one that read a skill. So the skill is not a condition of the
word; it is one component, and the line says what the run used: "skills read: none" or "skills read: fleet-audit". What
kube-agents adds in the no-skill case is still what the customer pays for: the authority limit, the unattended schedule,
the fleet collectors, the nightly measurement and the lapse. What it does not add there is the skill text, and the line
must not imply otherwise.

Three consequences. (1) The skill rating is a repair and cost signal, not the customer's word: it tells us where a skill
is needed on a model and where it is dead weight. (2) The no-skill arm (C5) decides per model and per skill whether the
text is necessary; where it is not, the skill shrinks to its scripts and rules or goes, because unread text still costs
tokens, maintenance and window restarts. (3) A capability the model carries on its own can leave with the next model
update; the window and the lapse exist for exactly that, and for a weaker model the same skill may be the difference
(the Gemini record shows both directions). Skills are therefore the per-model adaptation layer, kept where a supported
model needs them, measured rather than assumed.

What step 3 costs, beyond step 2: a private private line (a repository, a runner identity, a bucket and a seeded fleet
the authors cannot read: one pool project; the gap plan, H, option b), its cases (the panel's estimate is that a private-set
set roughly doubles the nightly's runs, against a nightly that cannot finish the 159 cases it has today, so its size is
a numbered decision when the first journey reaches step 2), the C6 safeguard sweep on every declared case (step 8),
and the named reviewer. The definition costs nothing today; the build does.

Options for the definition:

- a) **Step 3 as written** (private-set, authority, model, reproducible). Rec.
- b) **Step 3 without the private set**: cheaper and sooner; the claim stays open to "you tuned the skill to your own
  tests", which is the first question a reviewer asks (the narrative draft, "Questions a reviewer will ask").
- c) **Do nothing: keep "eval-tested"** (decided 10-19, D4) and return when one journey reaches step 2; none has today.
  Renaming step 2 "certified" is rejected by that decision.
  Principle: a certified claim is one a stranger can verify from the record without trusting the author.

One hole in the ladder with no owner yet (gap plan D6): what the line shows for the model a default install runs
(Gemini Flash), and whether the CI model and the installer default should be the same model. Section 14, question 4.

### 3.1 The word: what customers can be guaranteed, and what "certified" would promise

Customers ask for a guarantee, and "certified" reads to many of them as "guaranteed". The word is also overloaded in
this industry, with four meanings that have nothing to do with each other: a person's exam (CKA, the Google
Professional certifications), a conformance programme for a distribution ("Certified Kubernetes"), a compliance
attestation of an organisation's controls (SOC 2, ISO 27001, FedRAMP), and a vendor's partner or solution badge. None of
them promises an outcome, and a model-driven operator cannot promise one either. What it can promise splits into three
kinds, and the vocabulary should follow the kind:

| Kind of promise     | What it covers                                                                                                                                                              | How strong                                                                                                     | The word                                                                                                                   |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **A guarantee**     | The authority limit: read-only identity, the proxy that refuses every write verb, every change as a pull request a human merges; nothing it does is applied                 | Hard. Enforced outside the model, testable on every run, breakable only by a change to the install             | **guaranteed**: "guaranteed read-only", "guaranteed to propose, never apply"                                               |
| **A measured rate** | The outcome on a journey or capability: the window's lower bound on a named model and text, re-measured every night, with a lapse                                           | Statistical, like an SLO: a rate with a bound and a date, never a promise about one run                        | **measured** (public today as _eval-tested_): "measured 57 of 60 on Claude Opus 5.5 since 2026-11-20"                      |
| **An attestation**  | That the rate was produced the way we say: a private set, no forbidden action in the window, the model named, a reviewer outside the team who re-derived it from the record | As strong as the reviewer's independence and the record's openness; this is the compliance meaning of the word | **attested**, the top step; "certified" if the programme keeps that word, with its definition printed beside it every time |

This is the same three-step ladder as section 3 with the words made honest: the customer gets a guarantee about
authority, a measured rate about outcomes, and an attestation about how the rate was made. A certificate that promised
the outcome would be false the first night the model changed; the lapse rule exists because it would.

Options for the programme's name: a) keep "certified" for the top step and print its definition beside it
everywhere; b) use "attested" for the top step and never use "certified" except for the industry exams; c) do less:
"eval-tested" for everything above the floor, no top-step word until the private set and the reviewer exist. Rec: b
for the word, c for the timing, because "attested" says exactly what the top step is and is not yet claimed by the
Kubernetes vocabulary, and nothing meets the top step before 12-14 anyway. Principle: one word, one meaning, and the
guarantee word only where it is enforced.

## 4. The two metrics, defined so they can be counted

**HOOTL journeys** (human out of the loop). A journey counts as HOOTL when the agent takes it from trigger to outcome
with no human step, and the outcome is graded by evidence the deployed system returns, not by the agent's own report.
Three parts, each a yes or no per journey:

- _Trigger without a person_: a schedule, a cluster event, or a standing instruction. A chat question is not HOOTL;
  it is on-demand.
- _No human step before the outcome_: no approval, no answer to a question, no console click. A pull request the human
  merges is the end of the agent's part, so "a PR is open with the right change" is the HOOTL outcome; the merge is not.
- _Graded by evidence the product exports_: the ledger issue, the pull request diff against the planted defect, or the
  chat message, read on a schedule against a live install. Not a row in the runtime's own database: a check that reads
  Hermes's `executions.db` over `kubectl exec` proves a start, not an outcome, and dies with Hermes.
- _How it is run for grading_: the product's own trigger path. The first-run stage marks an audit due with the
  scheduler's `trigger_job`, and the next scheduler tick runs it through its schedule's own path with the same job
  definition (`agents/chat/scripts/oobe.py:29-37`); the scheduler and the stage are one path, only the clock differs.
  So a case can start a scheduled audit the product's way, three times a night, and the one rating rule applies: D1,
  at least 24 of 24 while the window fills (22 of 22 is the smallest all-pass count that clears 0.85), 57 of 60 when
  full, lapse below 0.70 on two nightly checks.
  One liveness line per audit ("last scheduled run at <time>", from the real clock) checks that the clock itself fires.
  The stronger form, one observation a night from the real clock on an install where nothing pauses it, is the later
  option (section 14, question 2).
  Reported as: HOOTL journeys available / journeys claimed, and for each the pass rate on the newest window.

**Certified capabilities** (the "certified employee/tasks" metric). A task is a journey or a skill with a rating: the newest 60
runs on one model, on its exact text and scripts, pass with a 95% lower bound of 0.85 or more (rule D1; at least 24 of
24 while the window fills). The word "certified" is reserved until a private private set and an independent reviewer
exist (D4); until then the public word is **eval-tested**. Reported as: tasks Rated / tasks tracked, per model, with
the date and the digest, and a lapse when the bound falls below 0.70 on two nightly checks.

Why two metrics and not one: HOOTL counts what the product does without a person; the rating says how reliably it does
it. A journey can be HOOTL and unrated (new, few runs) or rated and on-demand (version-control today).

## 5. Cost, latency and reproducibility: what is measured, and how each relates to "certified"

| Metric               | Measured today                                                                                                                                                       | Where                                                                                 | In the rating today                                                                                             | Proposed place in "certified"                                                                                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Latency**          | Yes, per run: agent seconds and first-turn seconds; the dashboard rolls up a per-case latency                                                                        | `results.json` `latency`; `gate.py:515-519`; `scripts/eval_dashboard/collect.py:1259` | No. A run that hits the case's agent cap (600 s) fails its checks, which is the only way time enters the record | The certified line carries the window's median and p90 run time. Lapse rule: p90 above 1.5x the value at certification on two nightly checks in a row flags "lapsed (latency)", reported, not blocking. |
| **Tokens**           | Yes, per run: input, cached, cache-write, reasoning, output, total                                                                                                   | `results.json` `tokens`                                                               | No                                                                                                              | The line carries median total tokens per run and the cached share. Same 1.5x lapse rule, reported.                                                                                                      |
| **Cost**             | No. Nothing converts tokens to money; the price depends on the customer's provider and model                                                                         | none (`bench/` has no price table)                                                    | No                                                                                                              | Reported as tokens, with a one-line conversion per model the customer can apply. We do not certify a dollar figure.                                                                                     |
| **Reproducibility**  | Partly. Three runs a night; the window of 60; the exact text pinned by digest; the model pinned by `setup_id`; the drift tier compares judged scores with a baseline | D1; `testing-strategy.md` §9 (drift); `evidence_store.py`                             | Yes: the lower bound on the window is the reproducibility measure for correctness                               | Certified requires the window (step 2) and the independent re-derivation (step 3d). Not controlled: provider-side model updates under the same name; they show as a lapse, which is the point.          |
| **Authority**        | Yes, per run: forbidden actions block on any run                                                                                                                     | gate rung 1; safeguards per case                                                      | Not in the rating                                                                                               | Required at step 3 (b): no forbidden action in any run of the window, plus the C6 audit-log sweep.                                                                                                      |
| **Quality (judged)** | Yes, per run: OutcomeScore and friends                                                                                                                               | `results.json` `scores`                                                               | No; the deterministic checks decide                                                                             | Stays out of the certified claim; shown beside it as context.                                                                                                                                           |

Why report cost and latency but not gate on them: a customer's bill depends on their model and provider, and a slow
run that still reaches the outcome is a cost, not a failure. A customer reads the typical run time and tokens on the
line and decides. Why gate on authority and reproducibility: those are the trust properties; a fast cheap wrong answer
is the failure this product cannot afford (`testing-strategy.md` §8).

Needed to deliver this: tokens written into the record (today the gate records agent and first-turn timing but no
token counts, `gate.py:515-522`: a small recording change), a tokens and latency roll-up per journey and per skill in
the scorecard (two columns), a lapse rule for each (two nightly checks, 1.5x), and the tokens-to-price note per model
in the published line.

### 5.1 Agent trajectories: recorded today, graded for the route, not yet for stability

A trajectory is the ordered list of tool calls a run made, with their arguments and results, for the Planning Agent and
for every worker it delegated to. The harness records it whole for every run (`results.json` `trajectory`; the workers'
calls are captured in the pod and tagged, `bench/kube_agents_bench/worker_trajectory.py`). Today the record is used in
three ways, and not in a fourth:

| Use                                                                                                     | Today                                                                                                                                                                                                         | Where                                                              |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Route adherence per case**: the named script ran, the named tool was called, no forbidden command ran | Yes, deterministic, blocks on any run                                                                                                                                                                         | `tool_called`, `worker_commands` checks; the gate's authority rung |
| **Judged tool use**: did the agent call tools sensibly                                                  | Yes, a judged score, context only                                                                                                                                                                             | `ToolInvocation`                                                   |
| **Re-grading after a check defect**: the typed commands are replayed against a corrected check          | Yes, on the laptop                                                                                                                                                                                            | the display-line re-grade used this week                           |
| **Stability across repetitions and across the window**                                                  | **No.** Nothing compares one run's route with the next. A journey can pass 60 of 60 by sixty different routes, or by a route that drifts a little every night until it fails, and the record would not say so | none; the one variance measure in the harness is the judge's       |

Why stability belongs in "certified" and not only the outcome: a customer runs the same journey every night. A route
that changes run to run is a route that costs a different amount each night, hits different quotas, and fails in a way
nobody has seen before. Reproducible for us means two things, and the second is the one we lack: (1) the same inputs,
the same exact text and the same model name give the same outcome at the rate the window states; (2) the route to that
outcome stays inside an envelope the window has seen.

Proposed trajectory measures, all derivable from the record we already keep:

| Measure                        | Definition                                                                                                         | Bound for a certified line (proposal)                                       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| **Tool set overlap**           | The set of distinct tools and scripts a run used, against the window's most common set (Jaccard)                   | median 0.8 or more; a run below 0.5 is flagged                              |
| **Step spread**                | Number of tool calls per run, p90 over median across the window                                                    | 2.0 or less                                                                 |
| **Loops**                      | The same command repeated more than three times in one run                                                         | 0 runs in the window                                                        |
| **Cost spread**                | Tokens and seconds per run, p90 over median (section 5)                                                            | 1.5 or less                                                                 |
| **Deterministic steps diffed** | Where a step is a script (a collector, `audit_report.py`), its output on the same fixture is diffed night to night | identical, or the difference is the fixture's own clock                     |
| **Envelope drift**             | The window's tool set or step median moving while the outcome still passes                                         | reported as an early warning; a provider-side model update shows here first |

What this is not: a demand that every run take one route. Different valid routes exist, and the hard part stays the
route checks the case already states (the named script ran, nothing forbidden ran). The envelope is learned from the
window per journey and model, and a certified line publishes it beside the pass rate: "median 14 tool calls, p90 21,
tool set stable at 0.9, no loops". Cost: a per-run summary (tool names, counts, step count) is a small extraction from
`results.json`; the roll-up is about 100 lines in the same `ratings.py` as the window; no harness change.

## 6. Good or bad against what: the baselines

| Judgement                                                        | Compared against                                                                                                                                                                                                                                                                                                                                    | Who set it                   | Have it?                                                              |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------------------------------------------------- |
| A run **passes or fails**                                        | **Planted truth.** The seeded fleet carries defects we planted (an over-permissioned binding, a Deployment with no PDB, a single-zone pool with a Pending backlog, a control plane one minor behind); the check asks whether the report, the ledger or the PR names that defect and nothing it should not. Absolute: the fixture is the answer key. | Us, per case, before the run | Yes: 230 cases, 134 on a planted fixture; `testing-strategy.md` §10.2 |
| A run **exceeds its authority**                                  | **Zero.** Any cluster write, Secret read or forbidden GitHub write fails the run; nothing absorbs it.                                                                                                                                                                                                                                               | Us                           | Yes: gate rung 1, safeguards per case                                 |
| A **judged score** (where the agent chose the words)             | **Our own past.** The case's score on `main` at the same key (model, judge, fleet, verifier, mode); must not fall much below it. Relative, and only to ourselves.                                                                                                                                                                                   | The record                   | Yes: `bench/kube_agents_bench/baselines.py`, the evidence store       |
| A **rating** (Rated, lapsed)                                     | **A fixed bar.** Lower bound 0.85 on the newest 60; lapse below 0.70 twice. The bar is a convention we chose, not a measured external standard.                                                                                                                                                                                                     | the project lead, D1         | Yes, locally                                                          |
| **Is the skill better than nothing?**                            | **The same model with the skill disabled through the product setting** (C5 through step 11b, `skills.disabled` behind one `PlatformAgent` field; the gap plan, D3 rejects the optimizer's directory move for this)                                                                                                                                  | Not yet                      | No. The setting is not built; one lease per skill version once it is  |
| **Is it better than another model?**                             | **A second model on the same cases.** Gemini 3.1 Pro for 29 nights is the only other record; it caught 8 check defects this week as a control.                                                                                                                                                                                                      | Not yet, as a rule           | Partly: the dashboard; not in the rating                              |
| **Is it as good as a competent operator?**                       | **A human baseline.** Nobody has run the cases by hand and recorded what a GKE SRE finds in the same time.                                                                                                                                                                                                                                          | Not yet                      | No                                                                    |
| **Is it better than "your own Claude plus the GKE MCP server"?** | The story's question.                                                                                                                                                                                                                                                                                                                               | Not yet                      | No; C5 is the nearest proxy                                           |
| **Does it find what customers lose sleep over?**                 | **Real customer failures** triaged into cases (gap plan step 10).                                                                                                                                                                                                                                                                                   | Not yet                      | No                                                                    |

So today "good" means: found what we planted, touched nothing it must not, and did not get worse than our own past.
That is a strong floor and a weak ceiling. Three things it cannot say: that the skill text adds anything (C5), that
the agent matches an expert (human baseline), or that the planted defects are the ones customers have (step 10).

**An answer key from outside the team: industry certification tasks.** The real exams cannot be sat by an agent, and multiple-choice exams (KCNA, KCSA, Google's DevOps and
Architect) measure the model, not the harness. The performance-task exams (CKA, CKAD, CKS) fit the bench: a task with a
scratch cluster, a change proposed as a PR and applied there, the end state checked. A pilot of 20 to 30 tasks across
the CKA curriculum domains, two arms (kube-agents against a bare model with the GKE MCP server), three runs each, gives
the first pass rate against a syllabus we did not write. It does not replace the private set (the tasks are public and a
skill can be tuned to them), but it is the cheapest external answer key, and the repo has none today.

What the plan adds, in order: (0) the certification-task pilot as the first external answer key, if approved;
(1) the second model as a standing control for check defects (cheap: the record exists);
(2) C5 through the product's disable setting on two skills in phase 3; (3) step 10, customer failures into cases, as the source of new fixtures from phase 2
on; (4) a human baseline on the first four HOOTL journeys: one SRE runs each journey by hand once and we record the
time and the findings as the reference line on the certified claim. Principle: a certified line states the answer key
it was graded against, and the answer key must come from somewhere a customer trusts more than us.

### 6.1 Other frontier models: the comparison we can make, and the one we cannot

kube-agents is not a model. It runs on the model the install chooses (Gemini, Claude, OpenAI, or an OpenAI-compatible
endpoint), so "better than a frontier model" is the wrong claim: it compares a harness with an engine. Two comparisons
are the right ones, and the record supports one of them today.

| Comparison                                                              | What it answers                                                                                     | Today                                                                                                                                                                                                                                                                                                                                                                                                                                    | How it is measured                                                                                                                                                  |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The same journeys across models, inside kube-agents**                 | Which model does which journey best, and what the install should run                                | Yes, two models: Gemini 3.1 Pro for 29 nights to 10-19 and Claude Opus 5.5 since 10-20, the same cases. On 14 shared skills Claude is 10 points or more ahead on 5, behind on 5, within 10 on 4; Claude is far ahead on the large audit skills, behind on some small ones; Claude opens the Cluster Agent skills on 2 of 11 cases where Gemini opened them on all 11. The installer default (Gemini Flash) has no line yet (decision 4). | The per-model rating: one window per journey, model and text; the dashboard's opened-versus-closed and who-is-ahead views                                           |
| **kube-agents on model X against the bare model X with the same tools** | How much the harness adds: the schedule, the authority limit, the fleet collectors, the house rules | No. Not measured; the earlier optimizer campaigns on Gemini found no gain from skill text alone in 5 of 7 suites, which is the nearest number                                                                                                                                                                                                                                                                                            | The no-skill arm (C5) for the skill text; for the whole harness, the certification-task pilot's second arm (a bare model with the GKE MCP server) on the same tasks |

What kube-agents can claim against any frontier model, with evidence: it runs that model unattended on a fleet with an
authority limit the model cannot talk its way past; it measures that model on your journeys every night and tells you
when a model update or a text change moved the result; and it lets you switch models and read the same line for the
new one. What it cannot claim yet: that it does a Kubernetes task better than the same model without it. That number
comes from the bare-model arm, and it should be run per release on the rated journeys, not every night.

Cost of keeping the first comparison honest: one nightly lane per model. The budget in section 10 holds one lane today
with a second half in flight; a Gemini Flash lane (decision 4) is the next, and a third model is a budget decision.

## 7. Effectiveness: does it find real problems and get them fixed?

Nothing in the plan so far measures effect; it measures correctness on planted defects. The proxies we have, and the
measures we lack:

| Measure                                      | Definition                                                                 | Today                                                                                                                                                                                                                                                       | Source                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Detection on planted defects** (recall)    | Share of planted defects the journey names in its ledger or report         | High on Claude for the big audits: fleet-audit's 13 clean cases 39/39; the whole record per case on the dashboard                                                                                                                                           | the nightly                                                      |
| **False positives** (precision)              | Findings raised on a clean fleet or against a declared posture             | Partial: the declared-intent cases pass 9/9 on Claude for compliance and cost; no clean second fleet exists, so "silent on a clean fleet" is unmeasured for every scheduled audit                                                                           | cases; `DRAFTS.md:238-239`                                       |
| **PR acceptance**                            | Agent pull requests merged / opened, per journey, on real installs         | On our own install's GitOps repository, last 30 days: **0 merged of 18 opened** (6 open, 12 closed unmerged); the owner merged 3 of his own 4. A test install, so nobody is expected to merge, but it is the only real-world number we hold, and it is zero | `toshiowang-labs/gke-infra`, `gh pr list`, 10-26                 |
| **Findings acted on**                        | Findings accepted, snoozed or dismissed with a reason / findings surfaced  | Not computed; the findings queue holds the states                                                                                                                                                                                                           | `findings_queue.py` on each install                              |
| **Time to first finding**                    | Minutes from install to the first ranked report and the first audit ledger | Measured per case in the eval (the first-run audits start at onboarding); not reported as a product number                                                                                                                                                  | `oobe-first-run-audits`; first-24-hour spec says T+1 h and T+6 h |
| **Incidents found before a person**          | Stalls and warning events the agent reported before anyone noticed         | Not measured; no incident log on any install joins the agent's alert to a human's first action                                                                                                                                                              | needs a customer or a staged fleet                               |
| **Versus doing nothing, or versus a person** | The no-skill arm; a human run of the same journey                          | Not measured (section 6)                                                                                                                                                                                                                                    | C5; a human baseline                                             |

What this says: we can show that the agent finds what we plant and stays quiet on declared intent. We cannot yet show
that anyone merges what it proposes, that it finds a problem before a person does, or that it saves time. The PR number
on our own install is the uncomfortable one, and the cheapest to improve: a merge is the human's step, so the measure
for the agent is the quality of the PR (does the diff fix the planted defect, does CI pass on it), and the measure for
the product is how many a customer merges.

Proposed effectiveness counters, in order of cost: (1) PR acceptance and PR quality per journey from the GitOps
repositories we already read (one query); (2) findings acted on from the queue (one script, data exists); (3) silence on
a clean fleet, which needs a second clean fleet in the pool; (4) time to first finding as a product number from the
oobe record; (5) incidents found first, from a customer deployment with an incident log; (6) C5 and the human baseline.
Principle: report what the customer does with the output, not only whether the output was right.

## 8. Where the counters stand today (2026-10-26)

| Counter                                                                                                     | Today                                                                                                                                                                                                                                    | Source                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Capabilities and skills Rated on Claude Opus 5.5                                                            | 1 of 21 tagged skills: version-control, 42/42, 0.92, since 10-25                                                                                                                                                                         | scorecard 08:33 EDT 10-26 (local)                                                                                                                               |
| Skills tracked with a tag                                                                                   | 21 skills on 60 cases (71 prototype tags; not on `main`)                                                                                                                                                                                 | `proto/skills-tags`                                                                                                                                             |
| Eval cases on `main`                                                                                        | 230 cases, 129 of them declaring a planted fixture (`fixtures:` or a `prebuilt/` stack); 166 registered nightly, 159 after the inject-lane exclusions; 13 presubmit, 12 blocking                                                         | `bench/tasks`, `hack/eval/*.txt`                                                                                                                                |
| Journey tests against a live install                                                                        | `bench/cuj`: 4 obtainability journeys, 1 responsiveness check, and since 09:47 EDT 10-26 ten Web Console harness journeys with an ephemeral-cluster mode ([#3914](https://github.com/gke-labs/kube-agents/pull/3914)); manual, not in CI | `bench/cuj/README.md`, #3914                                                                                                                                    |
| HOOTL journeys: scheduled starts graded                                                                     | 5 audits, by one case (`oobe-first-run-audits` reads the cron run records of the five first-run audits: compliance, reliability, cost, stockout, upgrade retrospective)                                                                  | `bench/kube_agents_bench/oobe.py:51-115`                                                                                                                        |
| HOOTL journeys: scheduled outcomes graded on a stock install                                                | 0                                                                                                                                                                                                                                        | no check reads a clock-started run's ledger or chat line; the nightly pauses the other clock-started audits for the lease (`hack/ci_pause_scheduled_audits.py`) |
| HOOTL-capable journeys (trigger without a person, no human step before the outcome, an agent does the work) | 17: 10 scheduled audits, 3 watches that hand the work to an agent (stall watch, repo watcher, weekly readiness brief), 3 event-driven, 1 remediation cycle whose outcome is the open PR                                                  | `cron/jobs.json`: 11 of 22 jobs are `no_agent` scripts; a script with a unit test is a test, not a journey (AGENTS.md "Where tests go")                         |
| of those, graded in part by bench cases on the eval fleet                                                   | 14                                                                                                                                                                                                                                       | inventory §4, recounted by the panel                                                                                                                            |
| of those, with no registered case                                                                           | 2 audits with a case blocked on its fixture: networking ([#2755](https://github.com/gke-labs/kube-agents/issues/2755)), GCE ([#2483](https://github.com/gke-labs/kube-agents/issues/2483))                                               | inventory §8                                                                                                                                                    |
| On-demand journeys (a person asks in chat)                                                                  | 18, all with cases; 1 needs a confirmation (`/feedback`)                                                                                                                                                                                 | inventory §4                                                                                                                                                    |
| Promises in the docs with no journey test and no registered case                                            | 20 rows                                                                                                                                                                                                                                  | inventory §10                                                                                                                                                   |
| Chat-evidenced journeys readable from CI                                                                    | 0: no CI install has a chat platform (`scripts/validate_bench_cases.py:194-206`)                                                                                                                                                         | the stall watch, the daily recap and every chat line need a chat install                                                                                        |

## 9. Journeys: how many can run with no human, and which

Method: every journey the product claims (README, the site, the SOPs, the cron roster, the project lead's first-24-hour spec)
or tests (`bench/cuj`, bench cases) is one row in [`certified-journeys-inventory.md`](certified-journeys-inventory.md), with its trigger, its human
steps, how it is graded today, its owner, and a readiness word. 47 rows.

**How many can be HOOTL: 17.** They have a trigger that needs no person, no human step before the stated outcome, and an
agent does the work. Eleven of the 22 scheduled jobs are scripts with no model call (findings nudge, sa-role watch,
daily recap, feedback prompt, board health, workspace GC, chat-delivery watch, the readiness watch and review, and the
reconcile); they are tested as code, not as journeys, except the three that hand their result to an agent.

| Group                             | Count | Journeys                                                                                                                                                  | Graded today                                                                                                                                                                       |
| --------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scheduled audits                  | 10    | compliance, reliability, upgrade and patch readiness, cost, consistency drift, AI security, stockout, networking fabric, GCE fleet, upgrade retrospective | 8 have bench cases that grade the SOP's checks on the eval fleet; networking and GCE have none registered                                                                          |
| Watches that hand off to an agent | 3     | stall watch (a Cluster Agent card), repo watcher (an issue-resolver card), weekly readiness brief (a model turn)                                          | each has a case on a piece                                                                                                                                                         |
| Event-driven                      | 3     | warning event to triage to `apply` to PR; GitOps drift alert and triage; autoscaler stockout investigator                                                 | 2 have cases; the stockout investigator is off by default with no case                                                                                                             |
| Remediation cycle                 | 1     | audit opens the critical PRs unasked                                                                                                                      | the HOOTL outcome is the open PR whose diff fixes the planted defect; the close after a merge needs the human and is not counted. 3 ledger cases; no case grades an auto-opened PR |

**How many are HOOTL today, by the definition in section 4: 0 outcomes graded; 5 starts graded.** The nightly pauses
the clock-started audits for its lease, except the five first-run audits (compliance 06:20, reliability 06:50, cost
Mondays 07:50, stockout 09:20, upgrade retrospective Sundays 18:00 UTC), which still fire on the clock; nothing reads
their ledger as a scheduled outcome, and a mid-eval pull request from one of them is charged to unrelated cases
([#3020](https://github.com/gke-labs/kube-agents/issues/3020), open, unassigned). The live journey suite is manual, and
no CI install has a chat platform. The 17 run unattended on every customer install; nobody measures that they reach
their outcome.

**The other 22 journeys are on-demand** (18 chat journeys, 4 install and lifecycle steps). They are the "certified
tasks" population together with the skills. 17 of the 18 chat journeys have cases; the exception needs a confirmation
by design (`/feedback`).

**Seven of the 25 need a human next**, by design, after the outcome: reply `apply`, decide a finding, merge a PR,
run the upgrade. That is the product's authority model, not a gap: the HOOTL outcome is the report or the PR.

**Which first, and how, reusing what exists.** `oobe-first-run-audits` already starts all five first-run audits the
product's way three times a night and grades that they started. The outcome grade is five `ledger_issue_contains`
checks added to that same case, with one new `lookup:` field on the verifier (audit label plus a since-time, 40 to 60
lines), because today the verifier finds the ledger from the run's final message, which a scheduled run has no
(`verifiers.py:4075-4090`). Zero extra audit runs, no new stack, no new case, no product change. Each outcome check
carries its silence half: the planted defect is named and the declared posture is not. The upgrade retrospective's
scheduled outcome on the seeded fleet is silence (`upgrade_retrospective_sop.md:73,230`), so its check asserts no
report. A GitHub 429 on the lookup is infra, not a fail. The other five audits (AI security, drift, patch readiness,
networking, GCE) stay paused during the nightly and refuse a trigger (`arm.py:102-107`), so they wait for the install in
question 3. The stall watch and the event triage need a chat post, also question 3.

## 10. How we add journeys and scale the loop

Historical rate of new eval cases, by ISO week, first commit of each `task.yaml` on `main`: W38 8, W39 12, W40 15,
W41 26, W42 33, W43 101, W44 (to 10-26) 1. Total 230. The run budget is the binding constraint, not authorship:

- The nightly grades 3 runs per registered case. Its last normal night (10-23) finished 435 runs in 9.4 h; the three
  nights since launched 151 cases, finished about 305 to 328 runs in the 12 h Prow deadline, and recorded 22, 1 and
  26 cases, because the harness runs rep 1 of every case, then rep 2, then rep 3, and records a case only after rep 3.
- So the roster is past the ceiling now: at the last two nights' pace about 95 to 110 cases fit in the 12 h deadline at
  parallelism 6 (a 151-case round took 4.9 h, the second 6.4 h); 166 are registered, 159 after the inject-lane
  exclusions. Every case added past that removes a case from the record unless the budget grows.

Two rates, kept apart:

- **Journeys promoted to HOOTL-graded.** Zero until the outcome verifier exists (section 13, phase 1). After that, the
  five first-run audits first, started through the product's trigger path three times a night, so the usual 60-run
  rule applies; a journey clears 24 of 24 in eight full-record nights only if it passes every run, and the five audits
  pass far less than that today (the request-graded compliance audit passes 0.21 on Claude over 34 runs; fleet-audit's
  window reads 15 of 23), so the first graded journeys are expected to read Not yet for weeks; then about one or two
  new journeys a week, bounded by the nightly budget above and by the install in question 3 for the rest.
- **New eval cases.** Bounded by the nightly's run budget, below.

Levers, and who owns them: (1) **the record loss** comes from `finish_case` recording a case only after its third
repetition (`hack/ci-eval-pr.sh:3948-3950`); the repetition-major order itself is deliberate, because same-case runs
serialize on the task lock and parked two of four lanes for 12 minutes on 08-31 (`:3959-3963`), so "one sort key" is
not the fix; per-repetition recording or the launch hold-back bnaylor proposed on
[#3384](https://github.com/gke-labs/kube-agents/issues/3384) is, and [#3821](https://github.com/gke-labs/kube-agents/issues/3821)
and [#3940](https://github.com/gke-labs/kube-agents/issues/3940) (lapis2002) track the cut-off nights: teammates own
this; (2) **the second main job** is in flight, not an ask: the kube-agents half merged this morning
([#3934](https://github.com/gke-labs/kube-agents/pull/3934)) and the Prow half is open
(oss-test-infra#2741, 15 cases in `nightly-main-b.txt`); (3) presubmit cost control stays as is; (4) journeys graded
by `bench/cuj` run on a chat-capable install on a schedule of their own, not inside the nightly. Honest arithmetic: (1)
and (2) buy one-time headroom of about 40 to 70 cases (a second half at today's pace, less the cases that already fail
to record), spent in one to three weeks at the W41 to W43 pace; after that, every new case needs a third job or a
retired case. There is no standing "30 a week".

## 11. The certification loop, and what "testing in the loop" means here

Aligned with `docs/designs/testing-strategy.md` §9-4: every test answers one of three questions, authority (binary,
blocks on any run), correctness (measured over repetitions), drift (a recorded baseline). The unit is the case: one
question against a named fixture plus what the answer must contain; a journey is covered by one case or by twenty.
The gate's verdict ladder already exists (forbidden action first, then missing checks, then an admitted case failing
all three runs, then judged scores below baseline). Certification adds a window and a bar on top of that ladder.

1. **A case or a journey test exists first.** Red on `main` for the right reason, green three times on the fix, then
   registered (`eval_driven_development.md`). No fix without its case.
2. **Nightly repetition builds the record.** 3 runs a night on the exact digest; the window is the newest 60.
3. **Admission.** A case enters the blocking roster only after a measured clean streak under nightly load (a flaky test
   is less useful than no test; #3583 precedent).
4. **The rating is per model and per digest**, and restarts on any edit of the skill (D1); a persona or SOP edit outside
   the skill directory restarts nothing today (a known gap).
5. **Testing in the loop for behaviour fixes**: a red run must be seen on an install that serves the rated model. Today
   none of the three dev installs can serve Claude (checked 10-26); that is the first blocker to lift.
6. **The no-skill arm (C5)** decides whether a skill helps at all: the same cases with the skill disabled through the
   product's own setting (step 11b), never by moving a directory (the gap plan, D3); one lease per skill version.
7. **Publication**: a scorecard only after the pod reports the digests it loaded (step 11a) and one skill is Rated.

## 12. What customers want

From the one customer source we hold, the epic [#2597](https://github.com/gke-labs/kube-agents/issues/2597) (a
retail platform team before peak: upgrade rollout stalls, IaC and Config Connector compatibility, silent controller
deadlocks, SecOps guardrails, IaC-aware audits), the story's customer and security reviews
(a local review file (not in the repository)), the narrative's reviewer questions (the narrative draft, "Questions a reviewer will ask") and the first-24-hour target spec:

- **The journeys of #2597 first**: upgrade rollout that does not stall (the retrospective and the rollout gate), controller
  deadlocks found without an error (the stall watch), IaC-aware audits that respect declared intent, guardrails a SecOps
  team can read (the authority limit). The first HOOTL journeys should be drawn from this list, not from what is
  easiest to grade.
- **A line they can trust per journey and model**, with the bytes it covers and the date; and the answer to "which
  journeys pass on the model my install runs", which today is Gemini Flash for a default install and shows as untested.
- **Proof of authority**: no run modified a cluster, read a Secret or leaked a credential (C6, the safeguard sweep on
  every declared case; the gate already blocks a forbidden action on any run).
- **No tuning to the test**: a private private set and an editor that never sees planted names; the word
  "certified" waits for these (D4).
- **Quiet by default**: the first-24-hour spec caps the backlog at two critical items a day and three non-critical
  after 16:00, and stops adding until the backlog clears. A HOOTL journey that spams is a journey nobody keeps on.
- **A fix arrives as a pull request they merge**, never a direct change; so the HOOTL outcome is the PR, and the merge
  stays theirs.
- **A regression is reported before it ships** (a lapse, D5) and the owner is named (step 7).

## 13. Roadmap

Order: reuse the oracle that exists, cost every case against the nightly the plan itself calls full, and promise only
what the record can carry. One rating rule throughout: D1 (24 of 24 while filling, 57 of 60 full, lapse below 0.70
twice). Dates run from the cases' first nightly, not from a "first full-record night".

| Phase                                                         | Dates (EDT)                                                                               | What ships                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Owner                                                | Counter after                                                                 |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------- |
| 0. Fix the measurement, and the record's bookkeeping          | 10-26 to 11-02                                                                            | PR A as one case (`obtainability-design-quota-vs-capacity`, [#3128](https://github.com/gke-labs/kube-agents/issues/3128)) plus a question to bradhoekstra on [#2344](https://github.com/gke-labs/kube-agents/issues/2344) for the observability case his issue plans to rewrite; nine owner reports; Claude enabled on one dev project (a console step for the project owner); PR 1a, the `skills:` key, with the case digest defined as the digest of the declared checks and prompt, not the whole file, so the key's own landing restarts no window. The record itself: oss-test-infra#2741 and [#3384](https://github.com/gke-labs/kube-agents/issues/3384) are the eval crew's. The counters get an owner and a home now: `docs/designs/journeys.yaml` (one line per journey, the entity the rating is keyed on), `ratings.py` in ci-health over data.json's store block, a generated region in the eval dashboard; the record key is (skill digest, SOP digest, model, mode, case digest); the lapse path files an issue when a journey or skill sits below 0.70 on two checks (`nightly_bugs.py` files only three-night 0/3 reds today) | the author; eval crew                                | Rated (skills) 1; HOOTL-graded 0                                              |
| 1. Grade the five first-run audits' outcomes, zero extra runs | case edit this week; red on `main`, three greens, registration; first nightly about 11-09 | the `lookup:` field on `ledger_issue_contains` (40-60 lines) and five outcome checks, each with its silence half, added to `oobe-first-run-audits`; infra-vs-fail for the lookup (a GitHub 429 is infra); the retrospective's outcome asserted as silence; the write-attribution gap ([#3020](https://github.com/gke-labs/kube-agents/issues/3020)) is not multiplied because no audit run is added, and [#2704](https://github.com/gke-labs/kube-agents/pull/2704) (named writes only) is watched                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | the fleet-audits domain; the case owner by report    | HOOTL-graded 5 from 11-09; Rated 0 (the audits pass well under the bar today) |
| 2. Chat evidence, the paused five, and journey ratings        | 11-09 to 11-30                                                                            | question 3 decides the install with a chat app where the clock is not paused; on it, the stall watch and event triage outcome checks (chat post plus PR diff) and the five paused audits' outcome checks; the rating per journey and per skill from `journeys.yaml` and the store, with tokens (now recorded) and latency columns; the ledger header line "written by run <id>, started by <scheduler, onboarding, request> at <time>" in `audit_report.py` as the one thing a customer can read on their own ledger                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | the author; eval crew for the install                | HOOTL-graded 5 to 12 depending on question 3; Rated 0 to 2                    |
| 3. Behaviour fixes, value, and the pod's own report           | 11-16 to 12-14                                                                            | the gh-miss and dismissal persona fixes on the Claude-served install; D2 after [#3191](https://github.com/gke-labs/kube-agents/pull/3191); step 11b (the disable setting) and then C5 on version-control and fleet-audit; step 11a (the pod reports loaded digests); internal scorecard page                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | skill owners; the author; operator owner for 11a/11b | Rated (skills) 2 to 4; HOOTL-graded 5 to 12, Rated 0 to 2                     |
| 4. The word "certified"                                       | after 12-14                                                                               | the private set (H, sized in numbers against the nightly budget), the named reviewer, the C6 sweep; the first certified journey line                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | eval crew                                            | first public line                                                             |

Why "Rated 0 to 2" and not more: the request-graded compliance audit passes 0.21 on Claude (`compliance-rbac-overgrant`,
34 runs) and the fleet-audit skill's window reads 15 of 23, so the first graded journeys read Not yet for weeks; and
the text they are rated on changes almost daily (skills changed on 23 of the last 30 days, fleet-audit on 22, the five
SOPs on 10 to 12 each), so a 60-run window on a fixed digest cannot fill. Either the five SOPs and fleet-audit get a
freeze for the window, or the key tolerates a digest change when the declared cases are unchanged (question 5). The
probability that a true 0.93 journey clears 57 of 60 is 0.39.

Today versus 12-14, the one table: Rated (skills) 1 to 2-4; HOOTL-graded 0 to 5-12; HOOTL Rated 0 to 0-2; certified 0 to
0 (the private set is not built in this window). Worker time: phase 0 about one worker-week (the `journeys.yaml`,
`ratings.py` and the generated region are the bulk, 700 to 800 lines by the panel's estimate); phase 1 days, not weeks;
phase 2 about two worker-weeks plus the eval crew's install; phase 3 the skill owners' loops at about 1.5 h of install
time each, plus 11a and 11b for the operator owner.

## 14. Open decisions, under [#3978](https://github.com/gke-labs/kube-agents/issues/3978)

1. **Which claim may use the word "certified"?** a) Eval-tested, plus a private set we did not write, plus no forbidden
   action in any run, plus the model named, plus a named reviewer outside the authoring team who re-derives the number.
   Cost: the definition is free today; the private line is one pool project and a case set sized when the first journey
   reaches step 2 (the panel's estimate: it roughly doubles the nightly's runs). First line after 12-14. b) Do less: the
   same without the private set; cost zero; a reviewer can say we tuned the skill to our own tests. c) Do nothing: keep
   "eval-tested" (decided 10-19) and return when one journey reaches step 2; none has today. Rec: a as the definition
   now, and decide the private-set build only when the first journey reaches step 2, with the cost in numbers. Principle: a
   stranger must be able to check the claim from the record; data before options.
2. **How do we count a HOOTL journey?** a) One observation a night from the real clock, verified after 20 clean nights;
   needs an install where nothing pauses the clock. b) Do less: a case marks the audit due with the product's own trigger
   (the path the first-run stage uses) and grades the ledger; three runs a night; the usual 60-run window; one "last
   scheduled run at <time>" liveness line checks the clock. First work: one verifier and five cases, about two
   worker-weeks. c) Do nothing: keep counting starts, as today's one case does. Rec: b. Principle: measure the product
   path at the rate the record can carry; the clock is a scheduler detail that changes with the move off Hermes.
3. **How do we read chat evidence in CI, and grade the five audits the nightly pauses?** The code answers the cheap
   option: the gateway's stored-post table fills only when a chat platform delivers (`audit_chat_report.py` docstring;
   `validate_bench_cases.py:190-200` keeps the two chat-report cases out of CI for that reason). a) A fourth install with
   a chat app and the clock unpaused: one pool project, one Slack or Google Chat app with an owner and a secret on a CI
   install (a threat line to write), about two worker-weeks, first line about 11-30. b) Do less: only the five first-run
   audits are HOOTL-graded, in the nightly; chat and the paused five stay "not measured" and hand-run on a chat install.
   c) Do nothing. Rec: b now, a as a phase 2 decision with its cost in a pool project and an owner. Principle: name the
   install that can read the evidence before promising the count.
4. **What does the line say for the model a default install runs?** Today the nightly rates `claude-opus-5-5` and the
   installer default is Gemini Flash, so a default install's line reads "untested" (gap plan D6). a) Rate the installer
   default too: a second nightly lane on Gemini Flash, cost one more job's budget. b) Do less: show "untested" with the
   reason, and make the install's model choice carry its rating line. c) Change the installer default to the rated
   model; cost and billing move to the customer. Rec: b now, a when the nightly budget allows. Principle: no hidden
   result; the customer sees the line for the model they run.
5. **The window key when the text changes almost daily.** Skills changed on 23 of the last 30 days and fleet-audit on
   22, so a 60-run window keyed on the exact digest never fills for the audits. a) Freeze the five SOPs and fleet-audit
   for the window (about three weeks of no merges to those files). b) Key the window on the text and scripts the agent
   reads and runs, normalised (the 10-22 window-rule note, option c), so a test or comment edit does not restart it; a behaviour edit
   still does. c) Tolerate a digest change when the declared cases are unchanged (the panel's suggestion); cheaper, and a
   loosened SOP then keeps a stale line until a case fails. d) Keep D1 as is and accept that fleet-audit never rates.
   Rec: b, with the normaliser as the one piece of code; a freeze is a policy nobody keeps. Principle: key the rating on
   what the agent can see or run, nothing more and nothing less.

PR A after the panel: one case, not two. `observability-trace-latency-brokered` is the case [#2344](https://github.com/gke-labs/kube-agents/issues/2344)
(bradhoekstra) plans to rewrite, and the `after_result_pattern` lines die when the harness default lands, which restarts
the window once more; the right move there is a question to him on #2344, not an edit.

Folded or dropped after review: "make the record whole" is in flight and owned by the eval crew; "the first four journeys" is question 2's first
work item; "the five unverified journeys" are scripts with unit tests, tested as code, and their chat delivery is
question 3; "keep eval-tested" is the status quo inside question 1.

## 15. The questions senior management will ask, with today's honest answers

| Question                                                                                               | Honest answer today                                                                                                                                                                                                                                                                   | What changes it                                                                                                                        |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **1. After a month of this, what does a customer get that they did not have?**                         | One line they can check: "version-control on Claude: 42 of 42 since 10-25". No journey line yet. The audits already run on every install; nobody measures that they reach their outcome.                                                                                              | Phase 1: five audit outcomes graded nightly. Phase 3: the first verified journey.                                                      |
| **2. Is the skill library worth anything on a frontier model?**                                        | Not shown. On Claude, pass rates with the skill open and closed are the same on every comparable case; 80 of 179 version-control uses ran the script without reading the text. The rules and scripts carry the value; the how-to prose does not.                                      | The no-skill arm (C5) on two skills; cut each skill to rules and scripts if it confirms.                                               |
| **3. Why should anyone trust a test you wrote and grade yourself?**                                    | They should not, fully. We plant the defects, write the checks, and run the nightly. The checks were validated on one model and eight broke on another.                                                                                                                               | A private set the authors never see and a named reviewer outside the team: step 3 of the ladder. Until then the word is "eval-tested". |
| **4. You run 166 cases a night and the job dies at the deadline. Is the measurement itself reliable?** | No, not this week: three nights recorded 22, 0 and 26 cases. The fix is in flight (the split job, the recording order), owned by the eval crew.                                                                                                                                       | The first night that records every case sets every date in this plan.                                                                  |
| **5. What does it cost per night, per journey, per customer?**                                         | We record tokens and latency per run; nobody converts them to money, and the price depends on the customer's model. A typical run: minutes and tens of thousands of tokens; the nightly: about 300 to 435 runs.                                                                       | Two scorecard columns and a per-model price note; never a certified dollar figure.                                                     |
| **6. Which model are you certifying for, and is it the one you ship?**                                 | We rate Claude Opus 5.5 in the nightly; the installer default is Gemini Flash; a default install shows "untested". Our own dev installs cannot serve Claude.                                                                                                                          | Question 4: rate the installer default, or make the line follow the install's model choice. Enable Claude on one dev project.          |
| **7. How many of your 47 journeys actually work unattended?**                                          | Unknown as an outcome. 17 are built to run with no human; 5 have their start graded; 0 have their outcome graded; 20 documented promises have no test at all.                                                                                                                         | Phase 1 and 2 counts, and trimming or testing the 20 promises.                                                                         |
| **8. What stops the agent from doing damage at 3 a.m.?**                                               | IAM and the credential proxy, not the prompt: a read-only identity, no merge, every change as a PR; a forbidden action fails any run. The audit-log sweep that proves it across every run (C6) is planned, not built.                                                                 | Step 8: C6 on every declared case.                                                                                                     |
| **9. How is this different from the vendor's own benchmark page?**                                     | A vendor scores a model on public tasks. We score a journey on your fleet's kind of defects, on the exact text that shipped, every night, and the line lapses when the model or text changes. That is the claim only an operator product can make, and it is the one we have to earn. | Phase 3's internal scorecard with lapses; later the public line.                                                                       |
| **10. Why did it take a model change to find eight broken checks?**                                    | Because the checks were written against one model's habits and nothing re-validated them. A second model as a standing control was not a rule.                                                                                                                                        | Make the second-model control a rule of admission; report "Gemini on the same case" beside every red.                                  |
| **11. What is the headcount and the calendar?**                                                        | About two worker-weeks for phase 1, two for phase 2, the skill owners' time for phase 3, plus the eval crew's record fix and one pool project for the private set. First verified journey about 12-07; first certified line after 12-14 and only if the private set is funded.        | the project lead's answers to questions 1 to 4.                                                                                        |
| **12. What if the customer's incident is not one you planted?**                                        | Then we would not know. The fixtures come from us; one customer epic (#2597) is the only outside source so far.                                                                                                                                                                       | Step 10: customer failures triaged into cases; #2597's journeys first.                                                                 |
| **13. Does it do the same thing every night, or just get the right answer?**                           | Unknown. The route of every run is recorded, and the named script and forbidden commands are checked, but nothing compares one night's route with the next.                                                                                                                           | Section 5.1: tool-set overlap, step spread, loops and cost spread per window, published on the line.                                   |
| **14. Does any of this survive the move off Hermes?**                                                  | The definitions, the cases, the ledger checks and the ratings do. The scheduler clock, the pause script and the persona text are Hermes-side and are kept to the minimum.                                                                                                             | The trigger-path method in question 2 is chosen for this reason.                                                                       |

## 16. The plan for skills

The skills work so far lives in pieces: the gap plan's steps, the window rule, the hill-climb plan for the twelve low
cases, the dashboard, and this document's principle that skills are the per-model adaptation layer. This section is the
one plan.

**Thesis.** A skill is three things: _rules_ (house decisions the model would otherwise invent differently each run:
severity grades, declared intent, skew policy), _scripts_ (deterministic collectors and verbs: `fleet_upgrade_report.py`,
`vcs.py`, the audit collectors), and _how-to prose_ (the route, for a model that needs it). On the rated model today
the first two carry the value and the third carries the cost: unread text still spends tokens, and any edit restarts
the window. So every skill moves toward rules and scripts, and prose stays only where a supported model is shown to need
it. A skill is rated, not certified; the customer's word attaches to the journey or capability it serves.

**What we know per skill today** (Claude Opus 5.5, the local scorecard of 2026-10-26; "used" is the share of tagged
cases on which the model opened the skill):

| Skill                                                                                                                                                                                        | Window                                             | Used                                      | What the data says                                                                                                                                            | Action                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| version-control                                                                                                                                                                              | 42/42, at the bar                                  | all cases                                 | The one rated skill. 80 of 179 uses ran `vcs.py` without the text. One real miss: the model looked for `gh` against the skill's rule, 2 of 9 before the reset | Keep. No edit before the full window. Then the persona line for the `gh` miss, red and three greens on a Claude-served install. C5 first candidate |
| fleet-audit                                                                                                                                                                                  | 15/23                                              | all 17 cases                              | 13 cases pass every run; four fail every run on one check each, three of them defects in the SOP, the collector or the check (hill-climb cases 4, 5, 6, 11)   | Fix through the owners' reports; the collector text for the stockout ledger; no prose edit. C5 second candidate on the 13 passing cases            |
| submit-suggestion                                                                                                                                                                            | 53/60                                              | all 8                                     | Two cases drag it: the cluster-setting request never ends in a proposal; a refusal case 7/9                                                                   | Owners' cases; no skill edit indicated                                                                                                             |
| fleet-upgrade-verification                                                                                                                                                                   | 17/21                                              | all 7                                     | The rollout-stall wording and the kubectl survey after the script, both agent behaviour                                                                       | A persona line, not a skill edit; the script's verdict line pasted verbatim                                                                        |
| gke-workload-troubleshooting, gke-reliability, gke-stall-detection, gke-workload-security (Cluster Agent)                                                                                    | 12/12, 11/12, 6/6, 9/9 on the few cases that count | opened on 2 of 11, 2 of 4, 1 of 1, 1 of 1 | The agent passes without opening them; where it opens them, it passes too                                                                                     | Discovery first (D2), after [#3191](https://github.com/gke-labs/kube-agents/pull/3191) lands and one week of nights; no text edit before that      |
| capacity-obtainability, gke-compute-classes, kube-agents-observability, fleet-audit-reports, gke-alert-configuration                                                                         | 1/12, 9/15, 3/6, 0/6, 0/6                          | all                                       | Low for check reasons in four of five (hill-climb cases 1, 2, 3, 12) and one behaviour miss (the metric, case 7)                                              | Case fixes by the owners and one of ours; the metric miss stays a skill-adherence finding for the owner                                            |
| eight one-case skills (gke-backup-dr, gke-platform-security, manage-cluster, github-issue-resolver, inspect-repository, cluster-agent-lifecycle, gke-cluster-creation, gcp-config-connector) | 9/9 or fewer                                       | one case each                             | Frozen while the main nightly is cut off; 24 runs need 8 clean main nights                                                                                    | Wait for the record; add no case until the budget grows                                                                                            |
| the 30 untagged skills                                                                                                                                                                       | no window                                          | unknown                                   | No case names them; 23 of 53 skill names appear in no case at all                                                                                             | Tag or retire: the two-reader tags (PR 2) decide which have a case; a skill no case names gets a case or leaves the shipped set                    |

**The steps, in order:**

1. **Measurement on `main`.** The `skills:` key (PR 1a), the two-reader tags (PR 2), the anti-tuning check (PR 1b), and
   the rating calculation in ci-health (step 5) with the use rate and the "needed on this model: yes, no, unknown"
   column. Until then the scorecard runs locally each morning.
2. **Fix the measurement defects, not the skills.** The hill-climb plan: one case edit of ours, nine reports to owners.
   No skill text changes on a rating's account.
3. **Decide the window key** (section 14, question 5), because skills changed on 23 of the last 30 days and no window
   fills under the exact-digest rule for the audits.
4. **C5 on the two skills with data**, version-control and fleet-audit's passing cases, through the product's disable
   setting (step 11b) on a Claude-served install, one lease each. The result sets each skill's shape on that model:
   prose kept, shrunk to rules and scripts, or retired.
5. **Discovery for the Cluster Agent skills** (D2), only after #3191 and a week of nights show whether its rewrite
   changed the opened rate; then the smallest fix with red and three greens.
6. **The two persona fixes** (the `gh` miss, the dismissal), on the Claude-served install, with the case as the gate.
7. **Tag or retire the untagged thirty**, one decision per skill, from PR 2's reader output: a case, or out of the
   shipped set.
8. **Provenance and an authoring rule.** Every check in every SOP and readiness module gets a `source:` line: the
   Google guide or release note it comes from, or the named incident; a check with no source is labelled "maintainers'
   practice" and reviewed for retirement. Every skill change carries its red and three greens (already the repository
   rule), the anti-tuning check, and a note of which window it restarts; a change that only moves prose on a skill
   whose C5 shows no prose value is declined.

**Dates.** Steps 1 and 2 this week and next (PR 1a on the go; the reports on the go; PR 2 after 1a). Step 3 with the
five decisions. Step 4 after Claude is enabled on one project, about one lease per skill. Step 5 after #3191, not
before mid-November. Step 6 with step 4's install. Steps 7 and 8 follow PR 2, by the end of November.

**What this plan does not promise.** That the skill library beats a bare model: C5 answers that per skill and per
model, and the honest expectation from the record is "equal" for the prose and "needed" for the scripts. That every
skill gets a rating: the one-case skills and the untagged thirty wait on the nightly budget and on PR 2.

## 17. Hard problems: the difficulty tier the record does not have yet

**The hypothesis, and what supports it.** The nightly may be testing mostly easy cases, which would explain why the
skills show no effect: a strong model passes an easy case with or without help. The record supports this more than it
contradicts it. The optimizer's seven campaigns found no headroom over the bare model in five suites. On Claude, every
comparable opened-versus-closed cell is equal. Where the record does show a skill helping, it is on the weaker model and
on the harder cells: on Gemini, `obtainability-direct-query` passed 15 of 15 with the reliability skill open and 18 of
40 without it. Most cases plant one defect on a four-cluster fleet and ask for it by name; that is a test of
correctness, not of difficulty. No case carries a difficulty label, so the question cannot be answered from the record
today.

**What makes a GKE problem hard**, from the customer epic ([#2597](https://github.com/gke-labs/kube-agents/issues/2597))
and the drafts: a symptom with no error (a controller that stops making progress silently); a cause that needs a
chain (a webhook that blocks a drain that stalls an upgrade that strands a pool); knowledge the model does not carry
(the known-issues catalogue, the removed-API list, release-channel and skew policy, the capacity and calendar-mode
APIs); a fleet too large to read by hand (the benchmarks of 3 clusters and 200 workloads, 10 clusters and 2,000
workloads); a long horizon (a rollout over days with a soak and a retrospective); conflicting signals (a declared
posture beside a real finding, noise beside the one real alert); and hostile input (an object annotation that reads
like an instruction).

**Three tiers, one label per case** (a `tier:` field beside `skills:`, repo-only, read by the scorecard):

| Tier | Shape                                                                                                    | What it tests                 | Where the harness should matter                                                    |
| ---- | -------------------------------------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| T1   | One planted defect, named by the check, on the seeded fleet                                              | Correctness and authority     | Little; a bare model with the tools passes it                                      |
| T2   | Two or more signals, one of them misleading; a declared posture; a wording the model must choose against | Judgment and the house rules  | The rules: severity, declared intent, silence on a clean fleet                     |
| T3   | Fleet scale, a causal chain, a long horizon, or knowledge from a catalogue the model does not hold       | Tools, schedule and knowledge | The collectors, the catalogues, the schedule; a chat session cannot do this at all |

Today's record is almost all T1, with a handful of T2 (the declared-intent cases, the healthy-namespace silence
cases, the misleading-symptom crashloop case). T3 exists only as drafts and as the customer epic.

**Does the story change on hard problems?** It should, in both directions, and both must be shown. The pitch's claim
is that the harness matters most where the model alone fails: the catalogue, the collectors and the rules are what a
bare model does not have. The risk is the opposite: on a T3 problem the trajectory variance grows, the model takes its
own route past a rule more often (the group of seven in the hill-climb plan is this pattern at T1), and a confident
wrong answer costs more. A certified line therefore names its tier, and a T1-only certificate says so.

**What the plan adds:**

1. **The tier label** on every case, assigned by the case owner with one line of reason, in the same pass as the skills
   tags (PR 2); the scorecard reports pass rate, use and the no-skill arm per tier.
2. **Ten to fifteen T2 and T3 cases from the customer epic**, before any new T1: silent controller deadlock on a cluster
   with a hundred healthy workloads around it; a rollout stall whose cause is a fail-closed webhook two hops away; an
   IaC repository where Config Connector and a live change disagree; a declared posture beside a real over-grant; a
   ten-cluster readiness grade under the nightly's time limit. Each needs its fixture, which is the cost: a larger
   seeded fleet or a second fleet, sized against the nightly budget in section 10.
3. **Headroom per tier**: the bare-model arm (section 6.1) run on the T2 and T3 set first, because that is where a gap
   would show; a tier with no headroom is a tier the skills do not need to serve.
4. **Scale as its own tier of evidence**: the two fleet benchmarks run on a schedule with the time and token cost
   recorded, because "reads the whole fleet in one pass inside the budget" is a claim a chat session cannot match and
   the record should show it.

**How a customer comes to trust kube-agents over a bare Claude or GPT.** Not by a claim that it is smarter: underneath,
it is that model. By five things the bare model cannot show on the customer's fleet: an authority limit enforced
outside the model, so the worst case is a wrong pull request, never a wrong change; a record on the customer's kind of
problems at a named tier, with the bare-model arm beside it, so the gap is measured rather than asserted; a route that
stays inside an envelope the record has seen (section 5.1), so the behaviour is repeatable, not a good day; a lapse
when the model or the text changes, so a silent model update is caught by the record before the customer meets it; and
an answer key from outside the team (the syllabus, the private set, the reviewer) so the claim does not rest on our
own tests. The hard tier is where all five are tested at once, and it is the tier the record has not run yet.

## 18. The intake loop: from the last 60 days of support cases to journeys, cases and skills

Today the fixtures come from us. The only outside sources are the customer epic
([#2597](https://github.com/gke-labs/kube-agents/issues/2597)), the public GKE known-issues and release-notes pages
that feed the readiness catalogues, and the `/feedback` command. There is no regular path from what customers actually
hit to what the nightly grades. This section is that path. It runs monthly over the trailing 60 days, and every step
ends in an artifact the repository already knows.

**1. Intake (monthly, one owner).** An approved, anonymised export of the period's GKE support cases and postmortems:
category, symptom, root cause, time to detect, time to fix, whether a configuration change would have prevented it, and
the GKE version and feature involved. No customer identifiers leave the support system; the export is aggregate
patterns with one redacted example each. Access to support data is an organisational decision and the first
prerequisite; until it exists, the proxies are the public known-issues page, the release notes, the customer epics, the
issues customers file on the product, and the agent's own ledgers on consenting installs.

**2. Triage (weekly, the domain owners).** Each pattern is scored on four axes and sorted: how often it occurs; how
bad it is; whether a scheduled check could have seen it before the incident (the habit test); and whether the fix is a
declarative change the agent could propose as a pull request. A pattern that scores high on the first two and low on
the third is an emergency-room pattern and goes to triage journeys; high on all four is a habit pattern and goes to the
audits. The output is one line per pattern in the drafts backlog (`bench/tasks/DRAFTS.md`), with its support frequency
as the priority, and a gap type:

| Gap type              | Meaning                                                               | What it becomes                                                              |
| --------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Not covered           | No journey looks for it                                               | A new check in an existing audit, or a new journey; a tier 2 or 3 case first |
| Covered, did not fire | A journey should have caught it and did not                           | A case that plants the pattern (red), then the skill or SOP fix (green)      |
| Caught, wrong fix     | The finding was right, the remediation was not                        | A case that grades the pull request diff, then the fix                       |
| Knowledge missing     | A known issue, a removed API, a version behaviour the catalogue lacks | A catalogue entry with its source line                                       |
| Out of scope          | Not a configuration or operations pattern                             | Recorded with the reason, so the count is honest                             |

**3. Fixture (per pattern, the case author).** The pattern is planted on the seeded fleet or a prebuilt stack so the
check is exact: the planted object, the symptom it produces, and the end state a correct run reaches. Patterns that
need scale or a chain are the tier 2 and 3 cases of section 17; the fleet grows against the nightly budget of section
10, and a pattern that cannot be planted stays a draft with that reason.

**4. Case before change (the repository rule).** The case runs red on `main` for the pattern's reason. Only then does
the skill, SOP or catalogue change, and it lands with three greens and the case registered. A change to agent text
restarts that skill's window; the intake owner batches changes per skill per month to restart it once, not weekly.

**5. Close the loop (monthly, with the counters).** Two numbers join the weekly report: the share of the period's
support patterns now covered by a graded journey or capability, by gap type; and, for consenting installs, the
findings the habit raised that match a pattern the support data says causes incidents. The second number is the one
that would show the emergency room emptying, and it needs an install where the ledger can be read back, which is the
customer's-own-view step (section 1.2, step 11).

**Cadence and cost.** Monthly intake and scoring: about two days of one owner plus an hour per domain owner. Cases:
the usual authoring cost, one to three days each with its fixture, bounded by the nightly budget, so the intake
decides which patterns are worth a case and which wait. The first run of the loop can start on the proxies today; the
support export is the step that makes it real, and it needs the data agreement before anything else.

## Appendix A. Sources and numbers

- Journey inventory with file:line evidence: [`certified-journeys-inventory.md`](certified-journeys-inventory.md) (47 rows; counts; registered cases per
  domain; promises with no coverage; notes on stale files).
- Scorecard and dashboard: the local scorecard files (not in the repository), the local dashboard (not in the repository).
- Case rate per week: first commit of each `bench/tasks/<id>/task.yaml` on `upstream/main` 791b1c102, 10-26.
- Nightly throughput: build logs of 2113420200605913088 (10-23), 2113782591592075264, 2114144982938947584,
  2114507375510556672 (the downloaded nightly logs (not in the repository)).
- Rules: `docs/designs/testing-strategy.md` §9-4; `.agents/rules/eval_driven_development.md`; gap plan D1-D6, H.

## Appendix B. Review records

### B.1 Red-team (blind review of draft 1; 10 findings, 8 changed the plan)

| Finding                                                                                                                                                                | Changed                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| The nightly pauses the clock-started audits for its lease (`hack/ci_pause_scheduled_audits.py`); phase 1 as written could not read a scheduled run on the eval install | Phase 1 rewritten around the four audits the pause leaves on the clock; phase 2 adds an install where the clock runs |
| No CI install has a chat platform; chat-line evidence is unreadable from CI                                                                                            | Chat-evidenced journeys moved to phase 2 behind decision 5                                                           |
| The `executions.db` pattern is Hermes-internal and proves a start, not an outcome; it contradicts section 4                                                            | Section 4 now requires evidence the product exports; the ledger header line is the mechanism                         |
| About 95 to 110 cases fit a night, not 145; the second main job already exists as `main-b` and is a Prow change                                                        | Section 10 corrected; decision 3 added                                                                               |
| "30 cases a week" is one-time headroom; "3 journeys a week" was an assumption                                                                                          | Section 10 rewritten with honest arithmetic                                                                          |
| REM-01's close needs the human merge; "PR open" is an outcome only if the check reads the diff                                                                         | Definition and §9 row corrected                                                                                      |
| Three of the 25 are `no_agent` plumbing scripts; networking and GCE have cases blocked on issues                                                                       | Count is 22; the "no verification" list is 5 with issue links                                                        |
| 24-of-24 passes a true 0.95 skill 29% of the time; "8 to 10 Rated by 12-14" not credible                                                                               | Targets cut; the 20-night window stated                                                                              |
| A cut-off night can leave the eval install's audits paused into the next day                                                                                           | Added to phase 1 as a fix in the resume path                                                                         |
| Mid-eval audit writes get charged to unrelated cases (#2611, #3020)                                                                                                    | The dedicated install in phase 2 has no GitHub-writing cases beside the audits                                       |

Not changed: the two-metric split; the ladder in section 3; the first-rating facts.

### B.2 Chief-of-staff check of draft 3 (10 facts corrected)

[#3978](https://github.com/gke-labs/kube-agents/issues/3978) is the tracking issue for this work (cited); the nightly split
is in flight ([#3934](https://github.com/gke-labs/kube-agents/pull/3934) merged, oss-test-infra#2741 open, 15 cases);
the repetition-major order is deliberate and the loss is in `finish_case`; `ledger_issue_contains` needs the run's final
message, so a new lookup is needed; no "started by" signal exists and none is needed under the trigger path; 11 of 22
jobs are `no_agent`, so 17 journeys, not 22; five first-run audits, not four; the private-set cost is now stated as a
sized decision; the customer source is #2597; one scope sentence; the D6 question added.

### B.3 Expert panel on draft 3 (five reviewers; unanimous concerns, nothing blocking; full table in Appendix C)

| Recurring item                                                                                                                          | Changed in draft 4                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 1 built what exists; `oobe-first-run-audits` already starts the five audits three times a night; a `lookup:` field is 40-60 lines | Phase 1 is five checks on that case plus the field; zero extra audit runs; "two worker-weeks" became days                                                                                                              |
| Dates from a "first full-record night" and two rating rules; "verified 3-5 by 12-14" had no basis                                       | Dates from the case's first nightly (about 11-09); one rule, D1; target "HOOTL-graded 5, Rated 0-2" with the reasons (pass 0.21; text changes 22 of 30 days)                                                           |
| C5 by the optimizer's directory move contradicts the decided gap plan                                                                   | C5 through the 11b product setting everywhere                                                                                                                                                                          |
| No record key, lapse path, infra-vs-fail, owner or home for the counters                                                                | All four in phase 0 and 1: key (skill, SOP, model, mode, case digests), lapse issue below 0.70 twice, a 429 is infra, `journeys.yaml` + `ratings.py` + a generated region                                              |
| §2 unsourced and over-stated; nothing a customer can check on their own install                                                         | Every claim sourced or cut; the ledger header line returns in phase 2; "nothing before 11a" said plainly                                                                                                               |
| Counts and words                                                                                                                        | 14 graded in part; 159 a night; headroom 40-70; ten audits; five first-run audits; 129 planted; #3914's ten harness journeys; "private set", "HOOTL-graded", "capability (a bench case)" for the project lead's "task" |
| PR A edits a case #2344 plans to rewrite                                                                                                | PR A is one case plus a question on #2344                                                                                                                                                                              |
| Authority stated as observation only                                                                                                    | Enforced and observed, both on the line                                                                                                                                                                                |
| Question 3b already answered by the code (the stored-post table needs a platform)                                                       | Question 3 rewritten; option b is "the five audits only"                                                                                                                                                               |
| The window cannot fill while the text changes daily                                                                                     | Question 5 added with four options                                                                                                                                                                                     |

## Appendix C. Expert panel table

Five reviewers on draft 3; code on `upstream/main` 232703e92; line numbers refer to the 376-line draft 3 (+18 to +45 after line 157 in later edits).

| Member          | Verdict  | Blocking | Main concerns (plan line → evidence)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------- | -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Eval/bench      | concerns | none     | Phase 1 builds what exists: `bench/tf/prebuilt/audit-chat-report/arm.py:21,50,100-118` already fires any job with `trigger_job` and waits; `audit_report_stored` reads the report by `started_at`; `ledger_issue_contains` binds label and stamp; a label-lookup fallback is about 30 lines, not 150, and "two worker-weeks" (l.304) is days. Phase 1 cost and lane missing: each case fires a real audit and `finish` opens PRs on the seeded fleet (#3020 shape); the cases must declare `audit_streams:` or run in the writers lane; about 2-2.5 h a night serialized on stream locks beside `oobe-first-run-audits`' 95 min. Date vs rule conflict (l.298): cases cannot exist on the "first full-record night"; red + 3 greens + registration puts the first nightly at about 11-09; §4 (l.101-103) adopts D1's "24 of 24 while filling" while §13 says 60 runs (Wilson: 22/22 is the smallest all-pass n at 0.85; 57/60 = 0.863). "HOOTL verified 3-5 by 12-14" (l.300, 303) has no basis: request-graded audits on Claude pass 0.21 (`compliance-rbac-overgrant`, 34 runs), fleet-audit skill 15/23; P(≥57/60 at true 0.93) = 0.39; cut to "graded 5; Rated 0-2". Upgrade retrospective's scheduled outcome on the seeded fleet is silence (`upgrade_retrospective_sop.md:73,230`). The trigger path stops at the five first-run audits (`ci_pause_scheduled_audits.py:21-33`; `arm.py:102-107` refuses a paused job). Tokens never reach the record (`gate.py:515-522`, SCHEMA.md). Counts: l.165 "17 graded in part" is 14; l.161 omits the 10 Web Console CUJ journeys (blocked on #2321); headroom 40-70 cases, not 100-145; l.26 "166" should be 159. Question 3b already answered by code (`audit_chat_report.py` docstring; `validate_bench_cases.py:190-200`).                                                                                                                                                                            |
| Customer        | concerns | none     | §2 story unsourced and over-states 4 of 5 claims (l.20 "nine audits" vs 10; l.26-27 "166 every night" is the roster, last nights recorded 22/1/26; l.28 example uses version-control's numbers, no journey has a line; l.28-29 "lapses" vs "new window"; l.33-34 "nothing else leaves" vs `security-and-iam.md:193-202`, corrected 10-22). The PR outcome is never observed in the customer's configuration: the sweep is off on every eval install (`hack/ci-deploy.sh:690-695`; #3439), so l.187 "no case grades an auto-opened PR" stays true through phase 4 by construction. No window key for a journey (l.95, 101-102, 257-258) while fleet-audit changes 22-23 days in 30; keyed on digests the window never fills, keyed on nothing a loosened SOP keeps a stale line. Phase 1 grades "found the planted defect" with no silence assertion (`testing-strategy.md:82-84`; ten no-finding cases exist). The customer-visible deliverable (ledger header line) was dropped in draft 3 (l.204-208, 346); nothing reaches a customer install before 11a in phase 3. §12 names #2597's journeys first, §13 picks the five audits without saying why. Authority clause (l.55, 135) states observation where the customer needs enforcement (override Security for that clause). C5 via "the optimizer's hide mechanism" (l.138, 261-262) reverts the gap plan:166-172's 11b decision.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| SRE/Day-2       | concerns | none     | The 60-run window cannot fill on the text rated: skills changed on 23 of 30 days (125 commits), governance on 19; `fleet-audit` 22 change-days; the five SOPs 10-12 each; the 12-14 targets need a freeze or a key that tolerates a digest change when declared cases are unchanged (l.50, 101-105, 257-258, 298, 303). §10 overstates headroom (40-70 cases, not 100-145; the 720-min deadline, not 480); phase 1 adds 15 real audit runs a night with no half, no `unit_cost_hint`, no retirement named; `oobe-first-run-audits` already starts all five audits x3, so phase 1 doubles them (fold the five ledger checks into that chain instead). The record key is decided in phase 3 after phase 2 rates on it (`baselines.py:356-377` has no skill or SOP digest; a switch to pod-reported digests restarts every window). No lapse path: `nightly_bugs.py` files only 0/3 three-night reds; a journey at 1/3 for ten nights lapses silently. Infra-vs-fail unstated: a ledger lookup failing on a GitHub 429 as FAILED lapses five journeys in one night (`KUBE_AGENTS_INFRA_FAILURE`). Stale: REM-01 unobservable while #3439 holds (l.187, 193); red-team row 10's "dedicated install" is not in §13. Counters have no owner or home; the rating runs on a laptop at 08:35 until phase 2.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Maintainability | concerns | none     | C5 contradicts the decided gap plan and the no-eval-only rule (l.138, 261-262, 300 vs the gap plan:166-170, 211: control arm only through the 11b product setting). Two rating rules over one record (bench-gate's 20 runs / 0.90 on the version key, `baselines.py:160,165`, vs D1's newest-60 / 0.85 / 0.70 in ci-health) with no file on `main` carrying D1, "Rated", "Eval-tested" or the ladder (zero hits; 12 local docs disagree). Phase 1 not costed against the plan's own ceiling rule (l.219-221): 3.75-5.4 h chain time a night; three hand-kept runner name lists per stack case (`ci-eval-pr.sh:2481, 2492, 2988`). New verifier duplicates bindings that exist; a new type bypasses the stream lock (`ci-eval-pr.sh:1342-1364` greps the literal type); a `lookup:` field on `ledger_issue_contains` is 40-60 lines. "No new measurement in the harness" wrong for tokens. "Per journey" has no data entity (`domains.yaml` has one `journey:` line per domain; the 47-row inventory is a local file; a `journey:` key in task.yaml edits teammates' cases). Liveness line has no reader. Hostages: PR A's `after_result_pattern` lines die with #2344/#3348 and their removal restarts three windows; phase 1 stacks write Hermes' cron store (#3655); D1 revisit options not in §14. Two roadmaps carry the same milestone with different mechanisms (roadmap-10-26.md §8 vs §13). Prose: labels before definition (C6, C5, D1, H, PR A/1a, REM-01, ci-health); "HOOTL-graded" undefined and "verified" was ruled out (D1-D6:27); the rating and lapse rules appear four times each; records disagree with the body (l.356 vs 346; l.360 "22" vs 164 "17"). Simpler design: one `lookup:` field, one parameterized stack, `docs/designs/journeys.yaml`, one `ratings.py` over data.json's store block, one generated region: 700-800 lines, no dashboard page, no schema bump, no install, vs 1,600+ lines, five stacks and an install. |
| Compatibility   | concerns | none     | PR A edits a case #2344 (bradhoekstra, open) plans to rewrite (`observability-trace-latency-brokered`; `after_result_pattern` on the display path #2344 deletes); both PR A cases are teammates' under the ownership rule; make PR A one case plus a question on #2344. Phase 1 multiplies the #3020 failure mode by five until #2704 (jayantid, open) lands (named writes only); each audit case needs a 600-1300 s `unit_cost_hint` (`test_ci_eval_nightly.py:431-450`); about 3.75 h a night on main-a. PR 1a's `skills:` key on about 60 teammates' cases may restart every window if the case digest is of the whole file (digest definition not on main). "private-set" already means a presubmit seat with no roster line (`eval-gate-roster.md`, 20 uses; bench-case-format.md:436, 498); "task" is a bench case; use "private set", "journey or skill", "HOOTL-graded". §8 "bench/cuj" row stale (#3914 merged 09:47 EDT added ten harness journeys with an ephemeral-cluster mode; lever (4) duplicates it). Phase 1 contract list incomplete (`bench/pyproject.toml:54`, `validate_bench_cases.py:593`, bench-case-format.md:96, CUSTOM-TASKS.md, `testing-strategy.md:125` "no case grades the scheduled path" becomes false). Phase 2 rating needs a key the store does not hold (`evidence_store.py:159` keys on `setup_id`); additive data.json field is compatible; four jayantid PRs on the same files. Dates: phase 1 waits on oss-test-infra#2741 (hold, hers to lift), the cut-off fix (#3384/#3821/#3940/#3936), #2704; 3a needs the eval crew; D2 needs #3191.                                                                                                                                                                                                                                                                                                                                                                     |

Security skip: confirmed for phases 0-2b (the by-label lookup reuses the runner's `issues: read` token; the rating runs in ci-health under the existing identity; `trigger_job` is the product's own path). Overridden for: the certified line's authority clause (state "enforced: RBAC read-only, IAM read-only, proxy refuses GitHub write verbs" beside "observed: 0 forbidden actions in N runs"); question 3a's fourth install (a chat-app secret on a CI install, no threat line); question 4a's Gemini lane and phase 4's private set (new identity, bucket, repository); the #3020/#2704 write-attribution gap phase 1 multiplies.
Performance skip: overridden for phase 1 (all five members): 15 real audit runs a night serialized on stream locks, 2-5.4 h; the plan's own §10 says the nightly is past the ceiling; no half, hint or retirement named; `oobe-first-run-audits` already runs the same five audits.

Verdict: unanimous concerns, nothing blocking, none approve as written. Five items recur across four or five members and go to the worker before the project lead reads it: (1) phase 1 reuses what exists (`audit-chat-report` stack, a `lookup:` field on `ledger_issue_contains`, or the five checks folded into `oobe-first-run-audits`' chain) and is costed and placed (lane, `audit_streams:`, `unit_cost_hint`, after #2704); (2) the dated targets are rewritten from the cases' first nightly under one rating rule (D1's 24-of-24 while filling), "verified 3-5 by 12-14" cut to "graded 5, Rated 0-2", and a freeze or a tolerant key named for the five SOPs and fleet-audit; (3) C5 through the 11b product setting, not the optimizer's hide; (4) the record key (skill digest, SOP digest, model, mode, case digest), the lapse rule, infra-vs-fail, and an owner and home per counter move to phase 0-1; (5) §2 is sourced or cut, and the customer keeps one thing to check on their own install (the ledger header line or an honest "nothing before 11a"). Counts to fix: 17 graded-in-part → 14; "166 every night" → 159; headroom 100-145 → 40-70; "Seven of the 25"; "nine audits" → 10; "first four" → five; bench/cuj row + 10 harness journeys; "134 on a planted fixture" → 129 with method. Terminology: "private set", "HOOTL-graded", "journey or skill". PR A: one case plus a question to bradhoekstra on #2344.

Rec: draft 4 with the five items above, then the project lead. Principle: reuse the oracle that exists, cost every case against the nightly the plan itself calls full, and promise only what the record can carry.

## Appendix D. Where the audit checklists came from: the compliance audit as the worked example

**Origin.** The governance SOPs arrived with the Platform Agent itself (PR #46, 2026-05-28) and have been edited in 29
commits since by several maintainers. A later requirements document (`docs/designs/fleet-anomaly-detection-checks.md`)
treats each SOP as the canonical list for its area and adds areas from a team's own incidents (a region lost to zonal
skew). Every check has the same shape: a flag rule, a do-not-flag rule with suppressions, a severity with its reason, an
impact sentence, a remediation kind, and the declared-intent override. So the lists are not random: they are curated
from the maintainers' production experience and incident history. But no check cites the document it comes from, and
no coverage map against a published benchmark exists. "Comprehensive" cannot be claimed without one.

**The compliance audit's 17 checks against the published guides** (the likely source by topic; the exact benchmark item
numbers vary by version and are to be verified when the source lines are written):

| Check                                                 | Likely source                                                           | Kind        |
| ----------------------------------------------------- | ----------------------------------------------------------------------- | ----------- |
| 2.1 privileged containers                             | CIS GKE Benchmark §5.2 (pod security); Pod Security Standards, baseline | posture     |
| 2.2 host namespaces                                   | CIS GKE §5.2; PSS baseline                                              | posture     |
| 2.3 hostPath mounts                                   | PSS baseline                                                            | posture     |
| 2.4 cluster-admin to non-system subjects              | CIS GKE §5.1 (RBAC)                                                     | posture     |
| 2.5 wildcard RBAC                                     | CIS GKE §5.1                                                            | posture     |
| 2.6 namespaces with no enforcing NetworkPolicy        | CIS GKE §5.3; GKE hardening guide                                       | posture     |
| 2.7 default ServiceAccount token automount            | CIS GKE §5.1                                                            | posture     |
| 2.8 Workload Identity off                             | CIS GKE §6.2 (identity); hardening guide                                | posture     |
| 2.9 legacy GCE metadata endpoint                      | CIS GKE §6.4 (node metadata); hardening guide                           | posture     |
| 2.10 public control plane without authorized networks | CIS GKE §6.6 (networking); hardening guide                              | posture     |
| 2.11 Pod Security `restricted` gaps                   | PSS restricted; CIS GKE §5.2                                            | posture     |
| 2.12 Config Connector stopped applying                | none published; GitOps operations                                       | operational |
| 2.13 image reference without specific bytes           | supply-chain practice (image pinning); not a CIS GKE item               | operational |
| 2.14 token mounted for an ungranted ServiceAccount    | CIS GKE §5.1 (automount only where needed)                              | posture     |
| 2.15 LoadBalancer publishing a management port        | network exposure practice; not a CIS item as such                       | operational |
| 2.16 binding whose subject is everyone                | CIS GKE §5.1; the NSA and CISA hardening guidance on anonymous access   | posture     |
| 2.17 Config Sync stopped applying                     | none published; GitOps operations                                       | operational |

Twelve of the seventeen are posture checks that a published benchmark also asks for; five are operational checks from
experience that no benchmark lists but a platform team wants. What the published benchmark asks for and this audit
does not check as posture: Binary Authorization enforcement, secrets encryption with a customer key, node
auto-upgrade and auto-repair, Shielded nodes and the hardened node image, private nodes and endpoints, logging and
monitoring enabled, legacy authentication disabled, Google Groups for RBAC. Several of these appear in the drift audit
as consistency facets (an outlier against the fleet majority), which is a different question from "is it on".

**The reliability audit's 24 checks** are the Kubernetes production-readiness list: requests and limits, budgets,
autoscalers, probes, spreading, single replicas, rollout strategies, Service selectors, termination grace, volume
contention. Google publishes this list across its GKE best-practice pages for reliable and cost-optimised workloads,
and the Kubernetes documentation carries the rest; again, no check cites them.

**What follows.** Step 9 of section 1.2 (a source line on every check) is this appendix done for all fifteen SOPs,
plus a coverage map per audit against its benchmark: which items are checked as posture, which as drift, which are
missing with a reason, and which are ours beyond the benchmark. That map is what turns "curated from experience" into
"follows the published guide, with these named additions and these named gaps".
