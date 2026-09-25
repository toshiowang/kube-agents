# The retrospective: an install that learns from its own work

> **STATUS — proposed; not implemented.** Nothing below ships today. This document is up for
> review before any code is written; the phases in §12 start only after it is agreed.

**Scope:** a scheduled job that reads what an install's agents did over recent days, finds work
they repeated or wasted, and proposes a change that would make the next run cheaper or better. A
person accepts or dismisses each proposal; only an accepted one reaches an agent.

**Owns:** learning that is specific to one install — its clusters, its operators' preferences, the
lookups its agents keep repeating. Defects in kube-agents' own code are
[#1284](https://github.com/gke-labs/kube-agents/issues/1284)'s job, which improves the product
from the repository side; this job never files one.

---

## In short

A CronJob, `kube-agents-retrospective`, runs a small Python package once a day. It reads the
install's Cloud Logging and Cloud Trace records, turns them into one record per task in a shape
that names no harness, and runs fixed detectors over those records: the same tool called with the
same arguments three times, a tool retried after an error, a finding the operator keeps dismissing,
a lookup repeated across days. A pattern becomes a proposal only once it recurs across tasks and
days. The Monday run writes a weekly report of open proposals. An operator accepts or dismisses
each one outside chat, and only then does a separate step apply it — as a shared memory fact, a
capability criterion, or a reviewed skill.

The job starts no agent and depends on Hermes only through one adapter file. Hermes' own
background learning is switched off, because on this deployment it almost never runs and what it
writes is deleted at the next pod start (§1).

## 1. The problem

An install repeats its own mistakes. Nothing records that the Platform Agent spent eleven tool
calls last Tuesday finding which project a cluster lives in, so it spends them again on Wednesday.
The pieces that come closest to fixing this are either inert or unconnected. Measured on one dev
install running Hermes v2026.9.14 on 2026-09-25:

- **Hermes' background skill review is on by default and almost never completes.** It ran to
  completion in 1 of 85 Platform Agent kanban sessions and in none on Cluster Agent profiles.
  Kanban workers exit with `os._exit(0)`, which kills the review thread before it finishes, and
  cron runs skip the review entirely. The curator runs only in the gateway process, which serves
  the Planning Agent's profile. Anything the review does write under a specialist profile's
  `skills/` is removed at the next pod start by step 2.6a of `deploy/shared/docker-entrypoint.sh`,
  which replaces that directory from the image on purpose.
- **Memory cannot learn from work.** [`memory.md`](memory.md) makes specialist memory read-only so
  a model cannot record its own conclusions as fact, and the Planning Agent writes only when a user
  asks. A specialist's `memory_candidates` nomination survives only if a user says "keep that".
  Installs default to `multiuser_memory` (`install.defaults.env`), which has no dates and no
  search; Hindsight is opt-in.
- **Capability self-learning is specified but not built.**
  [`capability-delivery-vehicle.md`](capability-delivery-vehicle.md) R5 describes an agent that
  proposes criteria changes from conversations. The criteria store in draft
  ([#1368](https://github.com/gke-labs/kube-agents/pull/1368)) has no pending-proposal state, and
  its `confirmed_by` field is a string nothing checks.
- **The data a harness-neutral job would read is incomplete.** Each specialist profile writes
  `profiles/<name>/logs/agent.log`, and Fluent Bit does not ship it. Every profile reports the same
  OpenTelemetry `service.name`, so a span cannot say which profile made it. The A2A bus, when
  enabled (`spec.mode: next`), keeps task events for its retention window W, 72 hours by default
  ([`spec-nats-deployment.md`](spec-nats-deployment.md)), and those events carry the request,
  progress narration, artifacts and final status — no tool calls, retries or token counts.

The closest prior art is the self-improvement job from #965, re-proposed as #1304 and closed. It
was a CronJob with a read-only identity, a ConfigMap ledger, a recurrence gate and report-only
output, aimed at kube-agents bugs. This design keeps that skeleton and points it at the install.

## 2. Goals and non-goals

Goals:

- Find recurring inefficiency across every agent profile on an install, from records the install
  already keeps.
- Name no harness outside one adapter. Replacing Hermes means writing a new adapter that emits the
  same events; the detectors, gate, ledger and appliers do not change.
- Apply nothing without a recorded human decision that code checks.
- Put what is learned where the agent already looks — shared memory, capability criteria, skills —
  rather than in a new store the agent has to be taught to read.

Non-goals:

- Defects in kube-agents' own code, prompts or skills that would affect every install. Those
  belong to [#1284](https://github.com/gke-labs/kube-agents/issues/1284). The telemetry fixes in
  §11 serve both jobs.
- Grading whether an answer was right. The job measures effort and repetition; correctness is the
  eval suite's.
- Real-time intervention. The job runs after the fact and changes nothing mid-task.
- Comparing two configurations of the agent against each other. That needs parallel installs and
  is a separate design (§12, Phase 4).

## 3. Options and the decision

| Option                                                         | What it learns                                                                 | Coupling to Hermes | Why not, or what blocks it                                                                                                                                                                                                                         |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A. Configure Hermes' skill review and curator                  | Skills from one process's recent turns                                         | Total              | `os._exit(0)` kills the review, and fixing that is a kanban patch this repository no longer takes. Cron runs skip it. The curator serves one profile. Step 2.6a deletes the output. Approval would live inside Hermes. No eval can see it          |
| B. Hindsight retain and consolidate                            | Facts                                                                          | Low (REST)         | Automated shared writes go against `memory.md`. Hindsight is opt-in. Consolidation merges facts in ways that lose detail                                                                                                                           |
| C. Make `memory_candidates` nominations durable without a user | Facts                                                                          | Kanban metadata    | Needs the Planning Agent to wake on child completion, which is a kanban patch, and kanban is being replaced                                                                                                                                        |
| D. Build capability vehicle R5 alone (#1368)                   | Audit criteria                                                                 | Low                | Covers criteria only, on the Platform Agent's profile only. #1368 is a draft with no pending state                                                                                                                                                 |
| **E. A harness-neutral retrospective job**                     | Repetition and waste across all profiles, routed to facts, criteria and skills | One adapter        | The telemetry gaps in §1, closed by the prerequisites in §11                                                                                                                                                                                       |
| F. Export Hermes session databases                             | Full transcripts                                                               | Total (`state.db`) | Another pod cannot mount the PVC, and the schema belongs to Hermes                                                                                                                                                                                 |
| G. Lengthen A2A task retention to 168 hours or more            | Task outcomes only                                                             | None               | W is a tenancy decision for the product, not this feature. Provisioning never edits an existing stream. The bus is off by default. Task events hold no tool-level data. The designed long-term archive is the audit exporter to Cloud Logging (G2) |

**Decision: E, with D and B as destinations rather than alternatives.** E produces proposals;
accepted ones are applied through #1368's criteria store (D), through Hindsight or a relayed memory
entry (B), or through a reviewed skill. A is switched off (§10). C and F are dropped. G becomes a
data source once the stage-2 audit exporter ships task events to Cloud Logging, which E already
reads; nothing here needs a longer window on the bus.

## 4. TaskRecord v1

Every detector reads one record per task. The record is the contract between harness adapters and
everything downstream, so it names no Hermes concept.

The job builds records from `ActivityEvent` (`admin_console/domain.py`), which the console already
produces from Cloud Logging rows and Cloud Trace spans through `normalize_logging_row` and
`normalize_trace` in `admin_console/telemetry.py`. Those normalizers are stdlib-only and already
know the Hermes span names and the `tool_call_audit` line format; the job reuses them rather than
parsing telemetry a second time. What they do not cover goes into
`retrospective/adapters/hermes.py`, the only file in the package that names Hermes.

| Field                                                             | Filled from today                                                          | Gap                                                                                                             |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `record_id`, `harness` (`hermes@<tag>`), `task_key`, `parent_key` | Trace `conversation.id` or session id; audit `task_id`; `subagent.*` spans | Joining a kanban task to its session is inferred, so every record carries `ActivityEvent`'s `attribution` level |
| `profile`                                                         | —                                                                          | P0-2 adds it to spans; P0-1 carries it in the shipped log's file path                                           |
| `trigger`, `started_at`, `ended_at`, `duration_ms`                | Root `agent` or `cron` span; audit timestamp                               | Until P0-1, an audit line re-shipped after a restart gets the ship time                                         |
| `llm_calls`, `tokens`                                             | `gen_ai.usage.*`, `hermes.turn.api_call_count`                             | Absent where an install ships logs but not traces                                                               |
| `tools[]`: name, outcome, duration, argument digest, error class  | `tool.*` spans and `tool_call_audit` lines                                 | Cluster profiles have spans only                                                                                |
| `skills`, `delegations`, `approvals`, `final_status`              | `skill.*`, `hermes.subagent.*`, `approval.*`, `hermes.turn.final_status`   | —                                                                                                               |
| `outcomes[]`: finding accepted or dismissed, pull request state   | —                                                                          | P0-5                                                                                                            |
| `goal_excerpt`                                                    | Prompt evidence on the root span, redacted and cut to 300 characters       | Held in memory for the run and never stored                                                                     |
| `coverage`: trace, audit, outcomes                                | `TelemetrySnapshot.incomplete`                                             | —                                                                                                               |

The argument digest is a hash of the tool arguments with identifiers, numbers and UUIDs normalised
out, so two calls that differ only in a timestamp compare equal and no argument value is kept.

`CloudTelemetryProvider` caps one load at 10 pages of 500 log rows and 10 pages of 100 traces. The
job therefore reads one day per run rather than a week at once, and the gate in §6 counts across
the ledger's stored days.

## 5. Detectors

Detectors are pure functions over a list of records. Each emits a subject — the part of the
pattern that identifies it, such as a tool name and argument digest — and a fixed route to one kind
of proposal. A model is not involved in detection.

| Detector                                                                         | Subject                     | Route                                                         |
| -------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------- |
| D1. The same tool with the same argument digest three or more times in one task  | tool, digest                | Skill                                                         |
| D2. A tool error followed by the same tool at least twice more                   | tool, error class           | Skill                                                         |
| D3. A turn or search budget exhausted                                            | profile, trigger            | Skill                                                         |
| D4. A failed delegation re-spawned with the same goal                            | target profile, goal digest | Skill                                                         |
| D5. The same approval pattern denied across tasks                                | tool, pattern               | Skill                                                         |
| D6. Cost above 1.5× the p90 of its (profile, trigger) class, with n ≥ 5          | profile, trigger            | Report only                                                   |
| D7. The same finding check dismissed three or more times                         | capability, check id        | Criteria                                                      |
| D8. The same read-only lookup subject in three or more tasks on two or more days | lookup subject              | Fact: the subject and where the answer lives, never the value |
| D9. The harness's own skill-writing tool called (`skill_manage` on Hermes)       | skill name                  | Skill review                                                  |

D8's rule matters for the memory bar in `memory.md`: a fact states where to find something ("the
billing export for project X is table Y"), never the live value the agent looked up, which would be
stale by the next run.

A pattern that points at kube-agents itself — a skill that always exhausts its budget on every
install, a tool that errors regardless of input — still becomes an ordinary proposal. The operator
who reads it dismisses it with the reason `upstream` and files it against the repository; the job
holds no GitHub credential and files nothing.

## 6. Recurrence gate and ledger

A detector firing once is noise. The gate decides when a subject has recurred enough to be worth an
operator's attention.

The fingerprint is the first 16 hex characters of `sha256(detector | profile class | subject)`,
where profile class collapses every `cluster-*` profile into one and the subject has identifiers,
digits and UUIDs removed. A fingerprint becomes a proposal when it has been seen in at least three
distinct tasks on at least two UTC days within seven days, or in at least five tasks within 28
days. A record with partial coverage counts as half a task, so a day with missing traces cannot
push a pattern over the line. A run opens at most five new proposals. A dismissal holds for 90 days
and reopens early only if the count reaches twice what it was when dismissed.

The ledger is one ConfigMap, `kube-agents-retrospective-ledger`, updated by compare-and-swap on
`resourceVersion` and retried on conflict, as #965 did. It holds fingerprints, per-day counts,
state and a title rendered from a fixed template per detector — no text taken from telemetry. The
reason is readability: the Platform Agent's ClusterRole reads every ConfigMap in the cluster
(`kubeagents:minimal:*` in `platformagent_manifests.go`), and a ledger that quoted tool output or
prompts would put that text in front of the agent looking like a kube-agents record. The size budget
is ConfigMap's 1 MiB; the job drops the oldest daily counts first and refuses to write past 900
KiB.

Proposal bodies, which do quote evidence, go to the job's stdout and therefore to Cloud Logging.
The Platform Agent's service account holds `roles/logging.viewer`, so it can read them — as it can
already read the telemetry they were built from. Readable is acceptable; what must not happen is a
proposal reaching an agent's prompt as memory, criteria or a skill without a decision, and §8 is
what prevents it.

## 7. Runtime and identity

The job is a Helm CronJob in the release namespace, off by default (`retrospective.enabled:
false`). It runs from the platform-agent image with the package copied in; it starts no Hermes
process.

| Setting    | Value                                                                                                                                                                                                                                                             |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Schedule   | `0 10 * * *` UTC (06:00 EDT); the Monday run also writes the weekly report                                                                                                                                                                                        |
| Job shape  | `concurrencyPolicy: Forbid`, `backoffLimit: 0`, 30-minute deadline, non-root, read-only root filesystem                                                                                                                                                           |
| Identity   | KSA `kube-agents-retrospective`, bound through Workload Identity to its own GSA holding `roles/cloudtrace.user` and a Logging view on the release's logs. Provisioned in `terraform/modules/kube-agents-iam` and wired into `examples/full-install`               |
| Kubernetes | A Role with `get` and `update` on the ledger ConfigMap and `get` on the decisions ConfigMap, each by `resourceNames`. No Secrets, no `pods/exec`, no PVC. The chart creates both ConfigMaps with `helm.sh/resource-policy: keep`, so the job never needs `create` |
| Network    | A NetworkPolicy with no ingress; egress to DNS, the metadata server and 443. LiteLLM is added in Phase 2 and Hindsight in Phase 3                                                                                                                                 |

The agent image fails its build if it contains `gcloud` (the cluster-CLI check in
`deploy/docker/Dockerfile`), and `CloudTelemetryProvider` gets its token through a
`CommandRunner` (`admin_console/connections.py`) that shells out to it. The job supplies its own
runner, `retrospective/gcp.py`, which answers the two token calls from the GKE metadata server.
Kubernetes calls use the in-cluster REST API through `urllib`.

## 8. Recording a decision

A second ConfigMap, `kube-agents-retrospective-decisions`, maps each fingerprint to `accepted` or
`dismissed` with a reason. No agent identity and not the job can write it: agent ClusterRoles grant
`get`, `list` and `watch` on ConfigMaps and nothing more, and the job's Role grants `get`. The
operator's ClusterRole can update any ConfigMap; it runs no model, and the Kubernetes audit log
records every writer, so who decided and when has a source.

Operators write decisions with `hack/retrospective.sh accept|dismiss <fingerprint>`, or from a
console page, and never through chat. A decision relayed by a model is text the model produced, and
text can be forged by anything that reached the model's context.

Every applier reads the decision in code before it writes, and records the decision id with what it
wrote. For capability criteria this supplies the pending state #1368 lacks and replaces its
free-text `confirmed_by` with something a reader can check.

## 9. Where accepted proposals go

| Kind     | Destination                                                                                                                                    | Applied by                                                                                                                                                                                                                                                                                                 |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fact     | Shared memory. The fact must pass `memory.md`'s bar: no live state, no conclusion the agent drew about itself                                  | On Hindsight installs, the job retains it with the tags `scope:shared`, `source:retrospective`, `decision:<id>` and `domain:<slug>`, using the request shape in `kube_agents_memory/client.py`. On `multiuser_memory` installs it stays a proposal the operator relays word for word to the Planning Agent |
| Criteria | #1368's `capabilities/<name>/criteria.json`                                                                                                    | `capability_criteria(set)`, gated on the decision id, which is written into the capability's `changelog.jsonl`                                                                                                                                                                                             |
| Skill    | A pull request to the operator's GitOps repository adding `learned-skills/<profile>/<name>/SKILL.md`. Merging the pull request is the decision | Markdown only; a proposal carrying scripts is refused. The entrypoint syncs the directory to `/opt/data/learned-skills/<profile>`, outside the tree step 2.6a replaces, and the Hermes adapter adds it to `skills.external_dirs`                                                                           |

The `domain:` slug on a fact is one of the eleven in [`domains.yaml`](domains.yaml), or `none`.
Memory is otherwise ungrouped — `multiuser_memory` is one list and Hindsight ranks by relevance —
so the slug is what lets an operator list, review or expire everything learned about cost, say,
without reading the rest. Each fact also keeps the date it was accepted, for re-checking facts that
may have gone stale.

## 10. Switching off Hermes' own loop

Hermes' background skill review and curator would otherwise write skills nobody approved, in a
place that is wiped on restart (§1). Both are switched off in `agents/{chat,platform,cluster}/config.yaml`:

- `skills.creation_nudge_interval: 0`. The review fires only when the interval is greater than
  zero (Hermes v2026.9.14, `agent_init.py`).
- `curator.enabled: false`, which `curator.is_enabled()` reads.

The platform profile's config is force-synced from the image at pod start. Existing cluster
profiles' configs are not, so the entrypoint gains a repair step beside the existing
memory-provider strip that sets both keys on each `profiles/cluster-*/config.yaml`.

`skill_manage` itself stays available to the model; D9 reports when it is used. Whether it may
write to image-shipped skills at all is [#1848](https://github.com/gke-labs/kube-agents/issues/1848)
and [#2034](https://github.com/gke-labs/kube-agents/issues/2034)'s decision, and this design defers
to it.

## 11. Prerequisites

Each prerequisite is useful without the rest of this design and ships as its own pull request.

- **P0-1. Ship specialist profile logs.** Add `/opt/data/profiles/*/logs/agent.log` to the Fluent
  Bit config the operator renders (`buildFluentBitConfigMap`), with a parser that keeps the line's
  own timestamp. Fluent Bit's tail database is on an `emptyDir` and re-ships after a restart, so
  the job de-duplicates on `sha256(file_path + line)`.
- **P0-2. Name the profile in spans.** Add a `kube_agents.profile` resource attribute in
  `deploy/shared/otel_config.py` and `agents/platform/scripts/cluster_agent_profile.py`, leaving
  `service.name` as it is so existing dashboards keep working.
- **P0-3. A NetworkPolicy for `hindsight-api`.** The chart gives the Hindsight database a policy
  but not the API. Phase 3 adds the job as a Hindsight client, and the policy that admits it should
  exist before a new client does.
- **P0-4. Carry the memory provider to the Planning Agent.** Either make the `PlatformAgent` CR's
  `memory.provider` reach `agents/chat/config.yaml`'s rendered overlay, or correct `memory.md` to
  say where the choice is made.
- **P0-5. Log finding outcomes.** Emit one structured log line on every finding state change in
  `session_kv_server.py`'s patch path, so D7 has something to count.
- **P0-6. Switch off Hermes' loop** (§10). This changes agent behaviour and follows the eval loop
  in §13.

## 12. Phases

One bullet is one pull request.

**Phase 1: report only.** The job writes its ledger and stdout and nothing else.

- 1a. `retrospective/records.py`, `retrospective/adapters/hermes.py` and tests built on
  `admin_console/tests/activity_fixtures.py`; add `retrospective/tests` to `PYTHON_TEST_DIRS`.
- 1b. `retrospective/{fingerprint,detectors,gate}.py` with tests. All pure functions.
- 1c. `retrospective/{ledger,gcp,run}.py`.
- 1d. The chart template, values and schema (`enabled: false`), `tests/test_chart_retrospective.py`,
  the IAM module change, and the Dockerfile `COPY`.

**Phase 2: proposals and decisions.** Still nothing reaches an agent.

- 2a. `retrospective/propose.py`: each detector's fixed route, with an optional model-written draft
  through LiteLLM. Evidence is passed to the model as quoted data and the output is validated
  against a JSON schema.
- 2b. The decisions ConfigMap and `hack/retrospective.sh list|show|accept|dismiss`.
- 2c. Optionally, a console page.

**Phase 3: apply.** One route per pull request, each under the eval loop: 3a criteria, 3b facts, 3c
skills (the `learned-skills` sync, `external_dirs`, and the copy the sandbox needs).

**Phase 4: check the effect.** For each accepted fingerprint, compare its rate over the four weeks
before and after, and propose a revert when it did not fall. On one install that comparison cannot
separate the change from everything else that moved in those weeks. A firm answer needs parallel
installs running the same workload with and without the change, which is a separate design: the
admission webhook allows one `PlatformAgent` per cluster, so each arm needs its own cluster and
renamed service accounts, and `bench` scoring would need efficiency metrics it does not have today.

## 13. Verification and eval-driven development

Unit tests cover records, detectors, the gate, the ledger's conflict retry and size budget, and
redaction, using recorded Logging and Trace responses as fixtures.
`tests/test_chart_retrospective.py` checks the Role's `resourceNames`, the absence of Secrets, and
the NetworkPolicy. The operator's golden files cover P0-1.

On a live install:

1. After P0-1, `gcloud logging read` returns entries whose file path is under `/profiles/platform/`.
2. After P0-2, a Platform Agent worker's span carries `kube_agents.profile` when read through the
   Cloud Trace API as the job's service account.
3. `kubectl create job --from=cronjob/kube-agents-retrospective` writes ledger entries per profile
   with coverage, and three sessions per profile checked by hand against their transcripts match
   their records.
4. `kubectl auth can-i` shows the job's service account cannot read Secrets, exec into pods or
   update decisions, and the Platform Agent's cannot update the ledger or decisions.
5. An accepted criteria proposal survives a pod restart, and the changelog carries its decision id.

P0-1 through P0-5 and Phases 1 and 2 change no agent behaviour and take the eval exemption. P0-6
and each Phase 3 route change what an agent does, so each starts from a one-prompt bench case that
seeds the learned artifact as a fixture — a `criteria.json`, a Hindsight fact, a `learned-skills`
directory — and checks the agent uses it. It must fail on `main` and pass three times on the
branch ([`eval_driven_development.md`](../../.agents/rules/eval_driven_development.md)); it claims
the domain of the artifact it seeds, so a criteria case claims `fleet-audits`.

Two bench changes support this and are exempt from the loop: a `maximum_calls` bound on the
tool-called verifier, so a case can fail on repetition, and a setup step that seeds an artifact
before the prompt. Seeding also needs the opposite switch:
[#1730](https://github.com/gke-labs/kube-agents/issues/1730) asks for bench runs isolated from the
agent's memory of earlier runs, and learned artifacts are one more thing such a run must be able
to turn off.

## 14. Open questions

1. **Who decides.** Operators through kubectl and the console only, or is there a role for a
   reviewer group named in the CR?
2. **Facts without Hindsight.** Is "stays a proposal the operator relays" acceptable on
   `multiuser_memory` installs, or should the job write there too?
3. **Where learned skills live.** The Reviewed tier in the capability vehicle's R6 is not built.
   Until it is, is the operator's GitOps repository the right home, or a repository of its own?
4. **Criteria gate.** Should #1368 take the decision id as its gate now, or land first and adopt
   it in 3a?
