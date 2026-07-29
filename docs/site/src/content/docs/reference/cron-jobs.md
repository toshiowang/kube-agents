---
title: Cron jobs
description: Full annotated agents/platform/cron/jobs.json — the autonomous watchdogs.
sidebar:
  order: 2
---

`agents/platform/cron/jobs.json` defines the autonomous watchdog jobs. For the story of what they achieve together, see [Proactive autonomy](/kube-agents/overview/proactive-autonomy/). For how the schedule/prompt loop works, see [Autonomous watchdogs](/kube-agents/concepts/autonomous-watchdogs/).

## The shipping jobs

Generated from [`agents/platform/cron/jobs.json`](https://github.com/gke-labs/kube-agents/blob/main/agents/platform/cron/jobs.json).

<!-- BEGIN GENERATED: cron-jobs -->
<!-- Regenerate with: make docs-generate -- do not edit by hand. -->
<!-- prettier-ignore-start -->

| ID | Schedule | Cadence | Enabled | Prompt |
| -- | -------- | ------- | :-----: | ------ |
| `blueprint-sync` | `0 9 * * *` | Daily 09:00 | yes | Execute GKE blueprint alignment audit. Read '/opt/defaults/governance/blueprint_sync_sop.md' and perform th... |
| `compliance-audit` | `0 9 * * 0` | Weekly, Sunday 09:00 | yes | Execute fleet-wide security compliance audit. Read '/opt/defaults/governance/compliance_audit_sop.md' and s... |
| `policy-propagation` | `0 * * * *` | Hourly | yes | Propagate updated operational policies. Read '/opt/defaults/governance/policy_propagation_sop.md' and inspe... |
| `global-capacity-orchestrator` | `0 * * * *` | Hourly | yes | Execute cross-cluster capacity optimization. Read '/opt/defaults/governance/global_capacity_orchestrator_so... |
| `fleet-wide-cost-analysis` | `0 10 * * *` | Daily 10:00 | yes | Execute daily cost delta audit. Read '/opt/defaults/governance/fleet_wide_cost_analysis_sop.md' to aggregat... |
| `security-patch-orchestrator` | `0 11 * * *` | Daily 11:00 | yes | Run vulnerability and patch compliance scan. Read '/opt/defaults/governance/security_patch_orchestrator_sop... |
| `lifecycle-deprecation-manager` | `0 9 1 * *` | Monthly, 1st 09:00 | yes | Execute monthly toolchain lifecycle audit. Read '/opt/defaults/governance/lifecycle_deprecation_manager_sop... |
| `standardization-validator` | `0 10 * * 0` | Weekly, Sunday 10:00 | yes | Run weekly structural GKE alignment audit. Read '/opt/defaults/governance/standardization_validator_sop.md'... |
| `obtainability-audit` | `0 12 * * *` | Daily 12:00 | yes | Execute dynamic capacity pool alignment audit. Read '/opt/defaults/governance/obtainability_audit_sop.md' t... |
| `github-issue-resolver` | `*/30 * * * *` | Every 30 minutes | no | Superseded by the github-issue-poll job on the default profile, which polls deterministically and files a k... |

<!-- prettier-ignore-end -->
<!-- END GENERATED: cron-jobs -->

## The Chat Agent's jobs

Only the `default` (Chat Agent) profile's cron actually ticks. A job placed on
the `platform` profile never fires — silently, with `enabled: true` and
`last_run: None` forever. The Platform Agent still does the work; it is just
reached through the kanban board rather than through its own schedule.

So a second, smaller set of jobs lives in
[`agents/chat/defaults/cron/jobs.json`](https://github.com/gke-labs/kube-agents/blob/main/agents/chat/defaults/cron/jobs.json).
Every one of them sets `no_agent: true`: they run as plain subprocesses rather
than model turns, decide whether there is anything to do, and file a kanban card
assigned to `platform` when there is. Nothing is spent on a tick that finds
nothing.

`github-issue-poll` is the reason `github-issue-resolver` above is disabled.
Discovering that an issue exists is one `gh issue list` call, so it no longer
costs a Platform Agent turn every thirty minutes; `github_issue_gate.py` runs
the same `resolver.py poll` the skill has always used and files a triage card
only when the poll returns an issue. The skill itself is unchanged — the worker
picks it up at Step 2.

## Job schema

Each entry follows this shape:

```json
{
  "id": "blueprint-sync",
  "name": "Blueprint Sync",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "display": "0 9 * * *"
  },
  "prompt": "Execute GKE blueprint alignment audit. Read '/opt/defaults/governance/blueprint_sync_sop.md' and perform the daily GKE cluster compliance checks against the master blueprints.",
  "skills": [],
  "enabled": true
}
```

| Field                 | Type            | Purpose                                                                                                           |
| --------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------- |
| `id`                  | string          | Stable identifier used in observability and enable/disable ops.                                                   |
| `name`                | string          | Human-readable name for logs and Chat replies.                                                                    |
| `schedule.kind`       | string          | `"cron"` for the jobs above; the Chat Agent's jobs also use `"interval"` with `minutes`.                          |
| `schedule.expr`       | string          | Standard 5-field cron expression, evaluated in the pod's time zone (UTC unless overridden).                       |
| `schedule.display`    | string          | Display form (usually equal to `expr`).                                                                           |
| `prompt`              | string          | The literal message sent to the agent when the schedule fires.                                                    |
| `skills`              | array of string | Optional: skills to preload. Most jobs leave empty (the SOP loads what it needs).                                 |
| `enabled`             | bool            | Set `false` to disable without deleting the entry.                                                                |
| `deliver` (optional)  | string          | Chat delivery mode. `"all"` reports every run back to Chat; `"local"` reports nothing beyond what the job prints. |
| `no_agent` (optional) | bool            | Run `script` as a plain subprocess instead of starting a model turn. Chat Agent jobs only.                        |
| `script` (optional)   | string          | Filename under `$HERMES_HOME/scripts/`, required when `no_agent` is set.                                          |

## Editing

Edit `jobs.json`, then redeploy the workspace:

```bash
cd k8s-operator/scripts
./provision_08_deploy_platform_agent.sh
```

Or during development:

```bash
cd k8s-operator
make dev-rebuild-agent ARGS="platform"
```

The change is picked up on the next pod restart.
