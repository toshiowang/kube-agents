# First 24 hours: spec vs code

Spec: `first-24-hour.md`. Code: upstream `main` at [`db9be7a7`](https://github.com/gke-labs/kube-agents/commit/db9be7a7) (2026-10-05).

**56 spec items: 11 met · 2 code ahead · 21 built differently · 17 missing · 5 blocked by an existing repo decision**

✅ met · ➕ code ahead of spec · ⚠️ built differently · ❌ missing · ⛔ blocked by an existing repo decision

## 1. Pacing and notifications

| | Spec | Code today |
|---|---|---|
| ❌ | First report surfaces exactly **2** critical findings | Up to **5** items; every critical if there are more than 5; top 3 informational if nothing is critical or major |
| ❌ | At most **2** critical items per day | The daily 12:00 UTC reminder shows 2 (hard-coded). Chat alerts are capped per UTC day at **10** critical, **5** warning, **5** info and **5** drift. The 30-minute stall watch posts when it opens or clears a card (up to **3** cards per run) with no daily cap |
| ❌ | After **16:00**, up to **3** non-critical items if nothing critical is pending | No time-of-day rule and no non-critical quota; every schedule is UTC |
| ⛔ | Nothing new while non-critical items are pending | Not built; the findings-queue design rejected rationing ("every finding is registered") |
| ⛔ | Secondary drifts and optimisation advice stay queued until criticals are resolved | Nothing is held back while criticals are open. Audits post every finding to their ledger issue and to chat; drift alerts have their own cap of 5 a day. Only the 12:00 UTC reminder filters to criticals |
| ⚠️ | Platform teams can change these limits | Only the four daily alert caps can be changed (`ALERT_DAILY_LIMIT_*`); the reminder's 2, the report's 5, the 5 pull requests per audit run and the stall watch's 3 cards per run are hard-coded |
| ⚠️ | Only high-severity blockers reach chat | Warnings and criticals both post; info events are dropped from chat and counted in the weekday 21:00 UTC recap. The stall watch and the scheduled audits post with no severity filter |
| ⚠️ | Remediation pull requests wait for human approval | The product cannot merge. Each scheduled audit run opens up to **5** pull requests for critical findings with a manifest fix, without asking anyone |
| ⚠️ | The chat alert says a remediation pull request has been drafted | The alert is followed by an analysis ending "reply 'apply' to open a GitOps Pull Request"; the pull request comes after the reply |

## 2. Timeline

| | Spec | Code today |
|---|---|---|
| ❌ | **T+5 min**: one command, no manual steps | No stated install time (Helm alone waits up to 600 s for each of two releases). Terraform creates the Google Chat Pub/Sub topic, but the Chat app is connected by hand in the Cloud console, and the GitHub App and its KMS key must exist before install. By default a new cluster is created |
| ⚠️ | Workload Identity bindings with no manual intervention | Terraform creates the agent service accounts and their bindings. On an existing cluster, the installer only prints the steps to enable Workload Identity on the cluster and node pools |
| ⚠️ | **T+0**: the agent starts the conversation | Event alerts and the stall watch post from T+0, but only to a home channel, which is an optional install flag and empty by default. The greeting and the onboarding report wait for the first human message |
| ⚠️ | **T+1 h**: inventory done, first 2 findings shown | The sweep writes and ranks the inventory report (gke-labs/kube-agents#2085, gke-labs/kube-agents#2167). No completion time is stated; the report shows up to 5 findings and is delivered only after the first human message |
| ❌ | **T+6 h**: first remediation pull requests | The first audit that can open pull requests runs at the next 06:20 UTC, up to ~24 h after install, and opens them only for critical findings with a manifest fix. gke-labs/kube-agents#1867 (open) adds a run at install time |
| ⚠️ | **T+24 h**: two-way chat; the Planning Agent only delegates | Delegation works. The Planning Agent has no infrastructure tools but can comment on and unblock board cards and write memory; the restriction lives only in its config. An off-by-default CR flag (`platformFrontDoor`) sends chat straight to the Platform Agent with its full toolset |

## 3. Proactive detection

| | Spec | Code today |
|---|---|---|
| ❌ | Deprecated APIs, found on a schedule before GKE upgrades | The scheduled job was retired; an on-demand scan checks manifests in Git only. The weekly patch audit flags deprecated node image types, not APIs |
| ⚠️ | Over-requested CPU and memory against **14 days** of usage; opens pull requests | Weekly audit (Mondays 07:50 UTC) reads the peak over **7 days** from Cloud Monitoring and flags peak ≤20% of the request. A pull request opens automatically only for a critical finding (8 vCPU or 32 GiB reclaimable on Autopilot); the rest wait for `/remediate` |
| ✅ | Privileged containers | Daily compliance audit at 06:20 UTC (`privileged: true`, SYS_ADMIN), plus a Pod Security `restricted` gap check |
| ✅ | cluster-admin bound to default service accounts | Daily audit flags any non-system account bound to cluster-admin (broader than the spec) |
| ⚠️ | Missing Workload Identity annotation or static keys | Daily check is cluster-wide only; the per-workload check runs once, at onboarding. No scheduled check looks for static keys |
| ⚠️ | Single-replica workloads without a PDB | The daily PDB check needs **≥2** replicas; a single-replica Deployment behind a Service gets a separate minor finding |
| ➕ | Spot and Flex availability (spec: in development) | Already ships: daily 09:20 UTC, flags a Spot shape whose mean daily preemption rate is above 20% over a 30-day history. Flex checked on request. No On-Demand check, by design |
| ⚠️ | Scale-up failures (FailedScaleUp, zone out of resources, quota) | The daily 09:20 UTC stockout audit reads 24 h of autoscaler logs and flags out-of-resources, quota and IP-exhaustion errors as critical. The event watcher ignores FailedScaleUp but opens triage on FailedScheduling once the autoscaler records NotTriggerScaleUp. The stockout plugin is off by default |
| ⚠️ | ComputeClass advice for workloads pinned to one machine family | The daily 09:20 UTC audit flags ComputeClasses pinned to one family, with a manifest adding fallbacks. Workloads pinned by a `machine-family` nodeSelector are not flagged, and no fix sets `activeMigration` |
| ❌ | Volumes above **85%** with a linear forecast | Not built; `gke-observability` only advises creating such an alert in Cloud Monitoring |
| ❌ | TLS certificates expiring within **7 days** | Not built. Certificates in Secrets are blocked (agents cannot read Secrets); ManagedCertificates and Compute SSL certificates are readable under the viewer roles, but nothing checks them |
| ❌ | Image CVEs from Artifact Registry | Not built; the patch audit says "Never claim CVE coverage" |
| ⚠️ | Subnet IP exhaustion (spec: planned) | A daily 08:00 UTC job is told to flag a range with less than 15% free, but its command returns ranges without usage, and its script checks Private Service Connect only. An exhausted Pod range shows up only afterwards, in the stockout audit's log check |

## 4. Chat examples

| | Spec | Code today |
|---|---|---|
| ⚠️ | Why is a deployment failing readiness checks? | The troubleshooting skill has no readiness or probe step. `gke-stall-detection` flags a pod stuck at `Ready=False` after about 15 minutes but does not name the probe |
| ➕ | Spot/Flex availability and stockout risk (spec: planned) | Works (`capacity-obtainability`), including future-window planning |
| ✅ | Draft a ComputeClass pull request with Spot fallback | Design from `gke-compute-classes`, pull request through `submit-suggestion` |
| ⚠️ | Right-size limits from **7 days** of usage | The weekly audit reads 7 days of usage and sets requests to 2× peak, leaving limits unchanged. A chat ask gets a pull request only for a workload the audit already flagged; there is no on-demand 7-day read |
| ❌ | Who changed RBAC in the last 24 h? | No audit-log query for RBAC changes; `gcloud logging read` is allowed, so the agent can only improvise one |
| ⚠️ | Will workloads break on a 1.30 → 1.31 upgrade? | Checks manifests in Git, not running workloads. Deprecation Insights and `kubectl get --raw` are refused |
| ✅ | Any root or privileged pods in a namespace? | Covered by the compliance audit's checks |
| ⚠️ | Which nodes are under memory or CPU pressure? | `kubectl top nodes` usage only; no node-condition check |
| ❌ | Why does an Ingress return 502? | No troubleshooting content; `backend-services get-health` is refused |
| ❌ | Critical alerts across the fleet in 12 h, grouped by root cause | No alert or incident read and no grouping. `fleet-audit-reports` lists past audit findings, not alerts |
| ⛔ | Validate a Workload Identity binding against GCP IAM | The service-account side of the binding cannot be read (IAM API refused, no `gcloud iam` verbs) |
| ✅ | Terraform change to enable Dataplane V2 (spec: planned) | Not built, as the spec says |

## 5. Architecture and lifecycle

| | Spec | Code today |
|---|---|---|
| ⛔ | MCP tools only, no raw shell commands | Agents have a terminal; `kubectl` and `gcloud` run through the credential proxy. `git` and `gh` are gone from the sandbox: Git and GitHub go through broker verbs. The GKE MCP server is loaded alongside |
| ⚠️ | Envoy credential sidecars inject tokens | Envoy runs in a separate credential-broker Pod, not as a sidecar; the broker runs each command itself. The sandbox holds no credentials; no token-rotation rules |
| ⚠️ | Installs into existing GKE clusters | Creates a new cluster by default; an existing cluster needs Workload Identity and NetworkPolicy enforcement on first |
| ⚠️ | Step-by-step root-cause reasoning defined in `SOUL.md` | The Cluster Agent's `SOUL.md` requires it; the Platform Agent's, which the spec cites, does not |
| ❌ | Triage skill: trace cascading failures to one cause, silence the rest | No triage skill; duplicate alerts are merged only per pod and reason over 5 minutes |
| ❌ | Upgrades keep the persona, cron jobs and custom playbooks | `SOUL.md` and skills are overwritten from the image on every start; the image wins for every cron job it ships |
| ❌ | The agent refines its skills at runtime and keeps the changes | Edits are lost at the next restart |
| ❌ | Three-way merge of upstream and locally edited skills | The sync script wipes local edits; a maintainer runs it by hand |
| ❌ | MCP tool schemas checked at startup, mismatches posted to chat | Not built |
| ⛔ | Auto-approval of low-risk fixes (spec: planned) | The architecture spec says "there is no auto-merge for any tier" |
| ✅ | Skill regression tests | Exist as evals in `bench/tasks/` (69 cases), not in `tests/e2e/` |
| ✅ | Operator CRDs `kubeagents.x-k8s.io/v1alpha1` | Matches |
| ✅ | Read-only diagnostic access | Kubernetes get/list/watch; view-level GCP roles on every project in scope |
| ✅ | GKE hosted MCP endpoint | Loaded |
| ✅ | LiteLLM model gateway | Default, behind the `inference-gateway` Service |
| ✅ | Upgrades keep the data volume | Yes |

## ⛔ Existing repo decisions the spec would reverse

| Spec item | Decision it conflicts with |
|---|---|
| Nothing new while items are pending; secondary items queued | `docs/designs/inventory-findings-queue.md` §7.3 rejected rationing findings |
| TLS expiry check, for certificates stored in Secrets | Agents never get Secret access, and an admission policy blocks granting it |
| Workload Identity validation | The API policy refuses `iam.googleapis.com` |
| MCP only, no shell | The design gives agents a terminal whose `kubectl` and `gcloud` commands the credential proxy runs |
| Auto-approval of low-risk fixes | The architecture spec says there is no auto-merge for any tier |

## In the code, not in the spec

- Alerts over the daily cap never reach chat; the weekday 21:00 UTC recap says how many were withheld
- Findings reminder at 12:00 UTC every day
- Board-health post at 12:35 UTC every day
- One-time feedback prompt at 13:00 UTC, about 7 days after install
- Controller stall watch every 30 minutes: opens a card for the cluster's Cluster Agent and posts a line when it opens and clears
- Chat delivery watch every 30 minutes: opens a GitHub issue when scheduled reports fail to reach chat
- GitHub repository watcher every 10 minutes: files a card when an issue or pull request is waiting
- Event-watcher recap at 21:00 UTC on weekdays
