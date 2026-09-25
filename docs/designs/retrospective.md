# The retrospective: an install that learns from its own work

> **STATUS — proposed; not implemented.** Nothing below ships today. This document is up for review
> before any code is written; the phases in §12 start only after it is agreed.

**Scope:** a scheduled job that reads what an install's agents did over recent days, finds work they
repeated or wasted, and proposes a change that would make the next run cheaper or better. A person
accepts or dismisses each proposal; only an accepted one reaches an agent.

**Owns:** learning that is specific to one install — its clusters, its operators' preferences, the
lookups its agents keep repeating. Defects in kube-agents' own code are
[#1284](https://github.com/gke-labs/kube-agents/issues/1284)'s job, which improves the product from
the repository side; this job never files one.

---

## In short

A CronJob, `kube-agents-retrospective`, runs a small Python package once a day. It reads the
install's Cloud Logging and Cloud Trace records, turns them into one record per task in a shape that
names no harness, and runs fixed detectors over those records: the same tool called with the same
arguments three times, a tool retried after an error, a finding the operator keeps dismissing, a
lookup repeated across days. A pattern becomes a proposal only once it recurs across tasks and days.
The Monday run writes a weekly report of open proposals. An operator accepts or dismisses each one
outside chat, and only then is it applied — as a shared memory fact, a capability criterion, or a
reviewed skill.

The job starts no agent and depends on Hermes only through one adapter file. Hermes' own background
learning is switched off, because on this deployment it almost never runs and what it writes under a
specialist profile is deleted at the next pod start (§1).

## 1. The problem

An install repeats its own mistakes. Nothing records that the Platform Agent spent eleven tool calls
last Tuesday finding which project a cluster lives in, so it spends them again on Wednesday. The
pieces that come closest to fixing this are either inert or unconnected. Measured on one dev install
running Hermes v2026.9.14 on 2026-09-25:

- **Hermes' background skill review is on by default and almost never completes.** It runs only in a
  profile that has the `skill_manage` tool, so never in the Planning Agent, which disables its
  `skills` toolset, unless the experimental `platformFrontDoor` setting makes the platform profile
  the gateway. It ran to completion in 1 of 85 Platform Agent kanban sessions and in none on Cluster
  Agent profiles: kanban workers exit when their task completes, before the review thread finishes,
  and cron runs skip the review entirely. The curator runs from long-lived processes — the gateway,
  the web server, an interactive CLI — and never from a kanban worker. Anything the review does
  write under a specialist profile's `skills/` is removed at the next pod start by step 2.6a of
  `deploy/shared/docker-entrypoint.sh`, which replaces that directory from the image on purpose.
- **Memory does not learn from work.** [`memory.md`](memory.md) makes specialist memory read-only so
  a model cannot record its own conclusions as fact. Shared memory grows only through a
  `memory_retain` the Planning Agent's model chooses to make in the moment; nothing looks back over
  a week of tasks for what was worth keeping. A specialist's `memory_candidates` nomination survives
  only if a user says "keep that". Installs default to `multiuser_memory` (`install.defaults.env`),
  which has no dates and no search; Hindsight is opt-in.
- **Capability self-learning is specified but not built.**
  [`capability-delivery-vehicle.md`](capability-delivery-vehicle.md) R5 describes an agent that
  proposes criteria changes from conversations. No criteria store exists yet, and applying a
  proposed change safely needs one with a pending state and a confirmation it checks (§14, question
  4).
- **The data a harness-neutral job would read is incomplete.** Fluent Bit ships
  `/opt/data/logs/*.log`, which holds the Planning Agent's log; each specialist profile writes
  `profiles/<name>/logs/agent.log`, which is not shipped. Every profile reports the same
  OpenTelemetry `service.name`, so a span cannot say which profile made it. The A2A bus, when
  enabled (`spec.mode: next`), keeps task events for its retention window W, 72 hours by default
  ([`spec-nats-deployment.md`](spec-nats-deployment.md)). The protocol reserves an `activity`
  artifact for tool-call traces ([`spec-a2a-payloads.md`](spec-a2a-payloads.md)), but the Hermes
  bridge publishes only the `result` artifact, so on this harness the bus carries no tool calls,
  retries or token counts.

The closest prior art is the self-improvement job from #965, re-proposed as #1304 and closed. It was
a CronJob with a read-only identity, a ConfigMap ledger and a recurrence gate, report-only by
default, aimed at kube-agents bugs; it ran a model in a Hermes profile of its own. This design keeps
that skeleton, drops the model from detection, and points it at the install.

## 2. Goals and non-goals

Goals:

- Find recurring inefficiency across every agent profile on an install, from records the install
  already keeps.
- Name no harness outside one adapter. Replacing Hermes means writing a new adapter that emits the
  same records; the detectors, gate, ledger and appliers do not change.
- Apply nothing without a human decision recorded where no agent can write.
- Put what is learned where the agent already looks — shared memory, capability criteria, skills —
  rather than in a new store the agent has to be taught to read.

Non-goals:

- Defects in kube-agents' own code, prompts or skills that would affect every install. Those belong
  to [#1284](https://github.com/gke-labs/kube-agents/issues/1284). The telemetry fixes in §11 serve
  both jobs.
- Grading whether an answer was right. The job measures effort and repetition; correctness is the
  eval suite's.
- Real-time intervention. The job runs after the fact and changes nothing mid-task.
- Comparing two configurations of the agent against each other. That needs parallel installs and is
  a separate design (§12, Phase 4).

## 3. Options and the decision

| Option                                                         | What it learns                                                                 | Coupling to Hermes | Why not, or what blocks it                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A. Configure Hermes' skill review and curator                  | Skills from one process's recent turns                                         | Total              | Kanban workers exit before the review finishes, and changing that is a kanban patch while kanban is being retired ([`spec-subagent-profiles.md`](spec-subagent-profiles.md)). Cron runs skip it. The curator serves one profile. Step 2.6a deletes the output. Approval would live inside Hermes |
| B. Hindsight retain and consolidate                            | Facts                                                                          | Low (HTTP API)     | Automated shared writes go against `memory.md`. Hindsight is opt-in. Consolidation merges facts in ways that lose detail                                                                                                                                                                         |
| C. Make `memory_candidates` nominations durable without a user | Facts                                                                          | Kanban metadata    | Needs the Planning Agent to wake on child completion, which is a kanban patch                                                                                                                                                                                                                    |
| D. Build capability vehicle R5 alone (#1368)                   | Audit criteria                                                                 | Low                | Covers criteria only, on the Platform Agent's profile only                                                                                                                                                                                                                                       |
| **E. A harness-neutral retrospective job**                     | Repetition and waste across all profiles, routed to facts, criteria and skills | One adapter        | The telemetry gaps in §1, closed by the prerequisites in §11                                                                                                                                                                                                                                     |
| F. Export Hermes session databases                             | Full transcripts                                                               | Total (`state.db`) | Another pod cannot mount the PVC, and the schema belongs to Hermes                                                                                                                                                                                                                               |
| G. Lengthen A2A task retention to 168 hours or more            | Task outcomes only                                                             | None               | W is a tenancy decision for the product, not this feature. Provisioning never edits an existing stream. The bus is off by default. The Hermes bridge publishes no tool-level data. The designed long-term archive is the stage-2 audit exporter to Cloud Logging                                 |

**Decision: E, with D and B as destinations rather than alternatives.** E produces proposals;
accepted ones are applied through #1368's criteria store (D), through Hindsight or a relayed memory
entry (B), or through a reviewed skill. A is switched off (§10). C and F are dropped. G becomes a
data source once the stage-2 audit exporter ships task events to Cloud Logging, which E already
reads; nothing here needs a longer window on the bus.

## 4. TaskRecord v1

Every detector reads one record per task. The record is the contract between harness adapters and
everything downstream, so it names no Hermes concept.

The job reuses what the console already has in `admin_console/`: `CloudTelemetryProvider`'s
authenticated, paged, redacting reads of Cloud Logging and Cloud Trace, `normalize_logging_row` and
`normalize_trace`, and the `ActivityEvent` shape they emit. Those modules (`telemetry.py`,
`domain.py`, `connections.py`, `project_config.py`) are stdlib-only. `ActivityEvent` keeps a fixed
set of fields, though, and `normalize_trace` discards the token, call-count and delegation
attributes a record needs and drops spans with no session id. The Hermes adapter,
`retrospective/adapters/hermes.py`, therefore reads raw spans for those attributes, reusing the
provider's authentication, trace listing, paging and redaction. It is the only file in the package
that names Hermes, and its tests pin the attribute names from recorded spans, because Hermes
documents none of them.

| Field                                                             | Filled from today                                                                                                    | Gap                                                                                                             |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `record_id`, `harness` (`hermes@<tag>`), `task_key`, `parent_key` | Span `gen_ai.conversation.id` or session id; audit `task_id`; `subagent.*` spans                                     | Joining a kanban task to its session is inferred, so every record carries `ActivityEvent`'s `attribution` level |
| `profile`                                                         | —                                                                                                                    | P0-2 adds it to spans; P0-1 carries it in the shipped log's file path                                           |
| `trigger`, `started_at`, `ended_at`, `duration_ms`                | Root `agent` or `cron` span; audit timestamp                                                                         | Until P0-1, an audit line re-shipped after a restart gets the ship time                                         |
| `llm_calls`, `tokens`                                             | `gen_ai.usage.*`, `hermes.turn.api_call_count`, read by the adapter                                                  | Absent where an install ships logs but not traces                                                               |
| `tools[]`: name, outcome, duration, argument digest, error class  | `tool.*` spans; `tool_call_audit` lines for the Planning Agent                                                       | The Platform Agent's audit lines ship after P0-1; Cluster Agent profiles write none                             |
| `skills`, `delegations`, `approvals`, `final_status`              | `skill.*`, `hermes.subagent.*`, `approval.*`, `hermes.turn.final_status`, read by the adapter                        | —                                                                                                               |
| `outcomes[]`: finding accepted or dismissed, pull request state   | —                                                                                                                    | P0-5                                                                                                            |
| `goal_excerpt`                                                    | Prompt evidence on the root span, redacted and cut to 300 characters                                                 | Held in memory for the run and never written anywhere                                                           |
| `coverage`: trace, audit, outcomes                                | Per record: whether a trace and, where that profile's audit lines are shipped, an audit line were found for its task | —                                                                                                               |

The argument digest is a hash of the tool arguments with identifiers, numbers and UUIDs normalised
out, so two calls that differ only in a timestamp compare equal and no argument value is kept. The
arguments arrive redacted and cut short — at 1,200 characters on a span (`hermes_otel`'s
`preview_max_chars` default), 2,000 on an audit line and 8,000 in the provider — so a digest over a
truncated argument can merge two calls that differ past the cut.

The provider reads a window that ends now, with a length from a fixed set (1, 6, 24, 72, 168 or 720
hours), and caps a load at 10 pages per query: up to 500 rows a page on each of its two logging
queries and 100 traces a page on the trace query. The job reads the last 24 hours each run, or 72
when the ledger shows the previous run missing, with every query at its 10-page cap. A load that
hits the cap is reported in the run's output. Windows overlap and records repeat across runs; §6
counts each task once.

## 5. Detectors

Detectors are pure functions over a list of records. Each emits a subject — the part of the pattern
that identifies it, such as a tool name and argument digest — and a fixed route to one kind of
proposal. A model is not involved in detection.

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
distinct tasks on at least two UTC days within seven days, or in at least five tasks within 28 days.
The day is the UTC day the task started, not the day the job ran. A record with partial coverage —
no trace, or no audit line where its profile's audit lines are shipped — counts as half a task, so a
task seen through only one source cannot push a pattern over the line. Coverage is judged per
record, never from whether the whole load was truncated, so a busy day that hits the page cap does
not halve every count. A run opens at most five new proposals. A dismissal holds for 90 days and
reopens early only if the 28-day count reaches twice the count recorded with the dismissal.

The ledger is one ConfigMap, `kube-agents-retrospective-ledger`, updated by compare-and-swap on
`resourceVersion` and retried on conflict, as #965 did. For each fingerprint it holds, per UTC day,
two sets of 8-hex-character digests of the task keys that matched, one for full coverage and one for
partial, so a task seen by two overlapping runs, a manual run, or a log line re-shipped after a
restart counts once. Beyond that it holds state and a title rendered from a fixed template per
detector. A template interpolates only the profile class and subject names that match
`^[A-Za-z0-9_.:-]{1,64}$`; any other value is replaced by its digest. No free text is taken from
telemetry, because the Platform Agent's ClusterRole reads every ConfigMap in the cluster
(`kubeagents:minimal:*` in `platformagent_manifests.go`), and a ledger that quoted tool output or
prompts would put that text in front of the agent looking like a kube-agents record. Days older than
28 are dropped, and the job refuses to write past 900 KiB of ConfigMap's 1 MiB.

Proposal bodies quote evidence — tool errors, span attributes, and in Phase 2 a drafted fact or
skill — and some of it the agents cannot read today: the Platform Agent's service account holds
`roles/logging.viewer` and no Cloud Trace role, and prompt evidence can come from another user's
conversation. The bodies therefore go to a Cloud Storage bucket, created by the IAM module, where
the job's service account can create objects and operators can read them. None of the roles the
shipped permission sets grant the agent reads Cloud Storage. The job's stdout carries fingerprints,
counts and trace ids only. The weekly report is one more object in the bucket, and
`hack/retrospective.sh list` prints it.

## 7. Runtime and identity

The job is a Helm CronJob in the release namespace, off by default (`retrospective.enabled: false`).
It runs from the platform-agent image, which gains the package and the four `admin_console` modules
it imports; it starts no Hermes process.

| Setting    | Value                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Schedule   | `0 10 * * *` UTC (06:00 EDT, 05:00 EST); the Monday run also writes the weekly report                                                                                                                                                                                                                                                                    |
| Job shape  | `concurrencyPolicy: Forbid`, `backoffLimit: 0`, 30-minute deadline, non-root, read-only root filesystem                                                                                                                                                                                                                                                  |
| Identity   | KSA `kube-agents-retrospective`, bound through Workload Identity to its own GSA holding `roles/cloudtrace.user`, a Logging view on the release's logs, and object creation on the proposals bucket. Provisioned in `terraform/modules/kube-agents-iam` and wired into `terraform/examples/full-install`                                                  |
| Kubernetes | A Role with `get` and `update` on the ledger ConfigMap and `get` on the decisions ConfigMap, each by `resourceNames`. No Secrets, no `pods/exec`, no PVC. The chart creates both ConfigMaps with `helm.sh/resource-policy: keep` and no `data`, so the job never needs `create` and an upgrade's three-way merge leaves what the job and operators wrote |
| Network    | A NetworkPolicy with no ingress; egress to DNS, to the metadata server at both `169.254.169.254:80` and `169.254.169.252:988` as `github-minter.yaml` does, and to 443. LiteLLM is added in Phase 2 and Hindsight in Phase 3                                                                                                                             |

The agent image fails its build if it contains `gcloud` (the cluster-CLI check in
`deploy/docker/Dockerfile`), and `CloudTelemetryProvider` gets its token through a `CommandRunner`
(`admin_console/connections.py`) that shells out to it. The job supplies its own runner,
`retrospective/gcp.py`, which answers the two token calls from the GKE metadata server. Kubernetes
calls use the in-cluster REST API through `urllib`.

## 8. Recording a decision

A second ConfigMap, `kube-agents-retrospective-decisions`, maps each fingerprint to `accepted` or
`dismissed` with a reason and, for an accepted fact or criterion, the exact change: the fact's text,
or the criteria key and value. The operator writes that change, starting from the proposal's draft,
so what gets applied is what a person put there.

No agent identity and not the job can write the ConfigMap. Agent ClusterRoles grant `get`, `list`
and `watch` on ConfigMaps and nothing more, and the job's Role grants `get`. This rests on the
permission sets the install ships: GKE authorizes through IAM as well as RBAC, so an install that
grants the agent `roles/container.developer` or `roles/container.admin` — which the installer warns
about and does not refuse — lets it write here too, and §13 step 4 is the check. The kube-agents
operator's ClusterRole can update any ConfigMap; it runs no model, and the Kubernetes audit log
records every writer, so who decided and when has a source.

Operators write decisions with `hack/retrospective.sh accept|dismiss <fingerprint>`, or from a
console page, and never through chat. A decision relayed by a model is text the model produced, and
text can be forged by anything that reached the model's context.

## 9. Where accepted proposals go

Each route has an applier that is deterministic code, reads the decision itself, and records the
decision id with what it wrote. No model sits between the decision and the write.

| Kind     | Destination                                                                                                   | Applied by                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fact     | Shared memory. The fact must pass `memory.md`'s bar: no live state, no conclusion the agent drew about itself | On Hindsight installs, the job's next run retains the decision's text through Hindsight's HTTP API with the tags `scope:shared`, `source:retrospective`, `decision:<id>` and `domain:<slug>`, and with `observation_scopes` pinned to `[["scope:shared"]]` and the shared strategy, as `memory.md`'s shared writes are, so the extra tags do not split its observations from the rest of shared memory. On `multiuser_memory` installs there is no API to write through, so the fact stays a proposal the operator relays word for word to the Planning Agent |
| Criteria | The capability's criteria file in the store #1368 proposes                                                    | The kube-agents operator mounts the decisions ConfigMap read-only into the agent pod. A step there, run at start and on a timer, reads accepted criteria decisions from the mount and writes each key through the store's validation and learning policy, with `decision:<id>` as the confirmation. It calls the store's code, not the `capability_criteria` MCP tool, so no model is involved                                                                                                                                                                |
| Skill    | `learned-skills/<profile>/<name>/SKILL.md` in a repository the operator keeps                                 | The operator commits the drafted skill from the bucket and merges it through review; the merge is the decision, and `hack/retrospective.sh accept` records it in the ConfigMap for the ledger. Markdown only; a draft carrying scripts is refused. Phase 3c adds the read-only sync that brings the directory to `/opt/data/learned-skills/<profile>`, outside the tree step 2.6a replaces, and the Hermes adapter adds that path to `skills.external_dirs`                                                                                                   |

The skill route is the one whose decision record is git rather than the ConfigMap: review of a pull
request is already the stronger record, and duplicating it would add a second place to disagree.

The `domain:` slug on a fact is a slug from [`domains.yaml`](domains.yaml), or `none`. Memory is
otherwise ungrouped — `multiuser_memory` is one list and Hindsight ranks by relevance — so the slug
is what lets an operator list, review or expire everything learned about cost, say, without reading
the rest. Each fact also keeps the date it was accepted, for re-checking facts that may have gone
stale.

## 10. Switching off Hermes' own loop

Hermes' background skill review and curator would otherwise write skills nobody approved (§1). The
kube-agents operator pins two keys in the managed scope it already renders to `/etc/hermes`
(`renderConfigYAML` in `platformagent_manifests.go`):

- `skills.creation_nudge_interval: 0`. The review fires only when the interval is greater than zero
  and the profile has `skill_manage` (Hermes v2026.9.14, `agent/turn_finalizer.py`).
- `curator.enabled: false`, which `curator.is_enabled()` reads.

The managed scope is the right place because Hermes overlays it per leaf key on every config load,
for every profile in the pod, and refuses to save over it, so a model editing its own profile config
cannot turn the loop back on. The comment on `renderConfigYAML` admits a key only if it is the same
for every profile and beyond the agent's own repair; these two pass the first test and not the
second. They join the way `approvals.cron_mode` did, as a policy that is uniform by design, and the
P0-6 pull request widens that comment to say so. Setting the keys in
`agents/{chat,platform,cluster}/config.yaml` would not reach every existing volume either: the
Planning Agent's config is back-filled only for keys it lacks, so a volume that already sets the
interval keeps it; the platform profile is back-filled the same way when it serves as the gateway;
and cluster profile configs are not re-synced at all.

`skill_manage` itself stays available to the model; D9 reports when it is used. Whether it may write
to image-shipped skills at all is [#1848](https://github.com/gke-labs/kube-agents/issues/1848) and
[#2034](https://github.com/gke-labs/kube-agents/issues/2034)'s decision, and this design defers to
it.

## 11. Prerequisites

Each prerequisite is useful without the rest of this design and ships as its own pull request.

- **P0-1. Ship specialist profile logs.** Add `/opt/data/profiles/*/logs/agent.log` to the Fluent
  Bit config the kube-agents operator renders (`buildFluentBitConfigMap`), with a parser that keeps
  the line's own timestamp. This adds the Platform Agent's `tool_call_audit` lines; Cluster Agent
  profiles load no audit plugin, so their tool calls still come from spans alone.
- **P0-2. Name the profile in spans.** Add a `kubeagents.profile` resource attribute to each
  profile's `hermes_otel` `resource_attributes`, which `deploy/shared/otel_config.py` writes, and to
  the Cluster Agent profiles `agents/platform/scripts/cluster_agent_profile.py` stamps. The existing
  `kubeagents.agent_type` and `kubeagents.agent_name` come from the pod-wide
  `OTEL_RESOURCE_ATTRIBUTES` (`manifest_helpers.go`) and cannot differ per profile. `service.name`
  stays as it is so existing dashboards keep working.
- **P0-3. A NetworkPolicy for `hindsight-api`.** The chart gives the Hindsight database a policy but
  not the API. Phase 3 adds the job as a Hindsight client, and the policy that admits it should
  exist before a new client does.
- **P0-4. Carry the memory provider to the Planning Agent.** `agents/chat/config.yaml` names
  `multiuser_memory` itself, and `spec.harness.memory.provider` no longer reaches it, which
  `memory.md` and the site's `reference/config.md` still describe as reaching it. Either make the CR
  field reach the Planning Agent or correct both documents.
- **P0-5. Log finding outcomes.** Emit one structured log line wherever a finding changes state in
  `session_kv_server.py` — registration, surfacing, snooze expiry, verification and patch — so D7
  has something to count. Each line carries an `audit_event` key, which the provider's logging
  queries select on.
- **P0-6. Switch off Hermes' loop** (§10).

## 12. Phases

One bullet is one pull request.

**Phase 1: report only.** The job writes its ledger and stdout and nothing else.

- 1a. `retrospective/records.py`, `retrospective/adapters/hermes.py` and tests built on
  `admin_console/tests/activity_fixtures.py` and recorded spans; add `retrospective/tests` to
  `PYTHON_TEST_DIRS`.
- 1b. `retrospective/{fingerprint,detectors,gate}.py` with tests. All pure functions.
- 1c. `retrospective/{ledger,gcp,run}.py`.
- 1d. The chart template, values and schema (`enabled: false`), `tests/test_chart_retrospective.py`,
  the IAM module change, and the Dockerfile `COPY`, inside the image-layer budget.

**Phase 2: proposals and decisions.** Still nothing reaches an agent.

- 2a. `retrospective/propose.py` and the proposals bucket: each detector's fixed route, with an
  optional model-written draft through LiteLLM. Evidence is passed to the model as quoted data and
  the output is validated against a JSON schema.
- 2b. The decisions ConfigMap and `hack/retrospective.sh list|show|accept|dismiss`.
- 2c. Optionally, a console page.

**Phase 3: apply.** One route per pull request, each under the eval loop: 3a criteria (the in-pod
applier), 3b facts, 3c skills (the `learned-skills` sync, `external_dirs`, and the copy the sandbox
needs).

**Phase 4: check the effect.** For each accepted fingerprint, compare its rate over the four weeks
before and after, and propose a revert when it did not fall. On one install that comparison cannot
separate the change from everything else that moved in those weeks. A firm answer needs parallel
installs running the same workload with and without the change, which is a separate design: the
admission webhook allows one `PlatformAgent` per cluster, so each arm needs its own cluster and
renamed service accounts, and `bench` records token counts per run but does not yet score on them.

## 13. Verification and eval-driven development

Unit tests cover records, detectors, the gate, the ledger's conflict retry, task-key de-duplication
and size budget, and redaction, using recorded Logging and Trace responses as fixtures.
`tests/test_chart_retrospective.py` checks the Role's `resourceNames`, the absence of Secrets, the
ConfigMaps' empty `data`, and the NetworkPolicy. The kube-agents operator's manifest tests cover
P0-1 and P0-6.

On a live install:

1. After P0-1, `gcloud logging read` returns entries whose file path is under `/profiles/platform/`.
2. After P0-2, a Platform Agent worker's span carries `kubeagents.profile` when read through the
   Cloud Trace API as the job's service account.
3. `kubectl create job --from=cronjob/kube-agents-retrospective` writes ledger entries per profile
   with coverage; three sessions per profile checked by hand against their transcripts match their
   records; and a second manual run in the same hour leaves the task counts unchanged.
4. `kubectl auth can-i`, impersonating each Kubernetes service account, shows the job's cannot read
   Secrets, exec into pods or update decisions, and the Platform Agent's cannot update the ledger or
   decisions. The same checks run with each Google service account's own credentials, through
   service-account impersonation, cover the IAM half, since GKE authorizes those through IAM as well
   as RBAC. The Platform Agent's Google service account cannot read the proposals bucket.
5. An accepted criteria decision is applied within one timer period, survives a pod restart, and the
   store's changelog carries its decision id.

P0-1, P0-2, P0-3 and P0-5, and Phases 1 and 2, change no agent behaviour and take the eval
exemption; so does P0-4 if it corrects `memory.md`, and it takes the loop if it changes which
provider the Planning Agent loads. P0-6 and each Phase 3 route change what an agent does and follow
the loop in [`eval_driven_development.md`](../../.agents/rules/eval_driven_development.md): red on
`main`, green three times on the branch, and the case registered in `hack/ci-eval-pr.sh` with
`owner:` and a domain.

Each Phase 3 case seeds the learned artifact as a fixture — a criteria decision, a Hindsight fact, a
`learned-skills` directory — and checks the agent uses it; it claims the domain of the artifact it
seeds, so a criteria case claims `fleet-audits`. P0-6 has no artifact to seed. Its case sends the
Platform Agent, which has `skill_manage`, a task long enough to cross the review interval, and
checks that no skill was written. Whether that case can be made red on `main` reliably, given how
rarely the review completes, is open question 5.

Two bench changes support this and are exempt from the loop: a `maximum_calls` bound on the
tool-called verifier, so a case can fail on repetition, and a setup step that seeds an artifact
before the prompt. Seeding also needs the opposite switch:
[#1730](https://github.com/gke-labs/kube-agents/issues/1730) asks for bench runs isolated from the
agent's memory of earlier runs, and learned artifacts are one more thing such a run must be able to
turn off.

## 14. Open questions

1. **Who decides.** Operators through kubectl and the console only, or is there a role for a
   reviewer group named in the CR?
2. **Facts without Hindsight.** Is "stays a proposal the operator relays" acceptable on
   `multiuser_memory` installs, or should the job write there too?
3. **Where learned skills live.** The Reviewed tier in the capability vehicle's R6 is not built.
   Until it is, which repository holds `learned-skills/`, and what credential does the sync read it
   with?
4. **Criteria gate.** Should the criteria store take a decision id as its confirmation from its
   first version, or adopt it in 3a?
5. **P0-6's red.** If the review completes too rarely for a case to fail on `main`, is the managed
   scope pin, checked by the kube-agents operator's manifest tests, enough evidence on its own?
6. **Where the weekly report is read.** A bucket object nobody opens changes nothing. Should the
   report also reach the operator's chat channel, and through what path that does not pass through
   an agent?
