# First 24 hours: spec vs code

Spec: `first-24-hour.md`. Code: upstream `main` at `5e18d111` (2026-09-24).

**54 spec items: 11 met · 3 code ahead · 17 built differently · 18 missing · 5 blocked by an existing repo decision**

✅ met · ➕ code ahead of spec · ⚠️ built differently · ❌ missing · ⛔ blocked by an existing repo decision

## 1. Pacing and notifications

| | Spec | Code today |
|---|---|---|
| ❌ | First report surfaces exactly **2** critical findings | Up to **5** items; every critical if there are more than 5; top 3 informational if nothing is critical or major |
| ❌ | At most **2** critical items per day | The daily 12:00 UTC reminder shows 2 (hard-coded). Chat alerts are capped per UTC day at **10** critical, **5** warning, **5** info and **5** drift |
| ❌ | After **16:00**, up to **3** non-critical items if nothing critical is pending | No time-of-day rule and no non-critical quota; every schedule is UTC |
| ⛔ | Nothing new while non-critical items are pending | Not built; the findings-queue design rejected rationing ("every finding is registered") |
| ⚠️ | Platform teams can change these limits | Only the four daily alert caps can be changed; the 2, 5 and 5 are hard-coded |
| ⚠️ | Only high-severity blockers reach chat | Warnings and criticals both post; only info is dropped |
| ⚠️ | Remediation pull requests wait for human approval | The product cannot merge. The scheduled audit opens up to **5** pull requests per run without asking anyone |
| ⚠️ | The chat alert says a remediation pull request has been drafted | The alert is followed by an analysis ending "reply 'apply' to open a GitOps Pull Request"; the pull request comes after the reply |

## 2. Timeline

| | Spec | Code today |
|---|---|---|
| ❌ | **T+5 min**: one command, no manual steps | No stated install time (Helm alone waits up to 600 s for each of two releases). Google Chat Pub/Sub and the GitHub App are set up by hand in their consoles; by default a new cluster is created |
| ⚠️ | **T+0**: the agent starts the conversation | Event alerts post from T+0. The onboarding report waits for the first human message; with no home channel (every DM install), alerts go nowhere |
| ❌ | **T+1 h**: inventory done, first 2 findings shown | The inventory report is never written while #1872 is open, and it waits for the first human message |
| ❌ | **T+6 h**: first remediation pull requests | The first audit runs at the next 06:20 UTC, up to ~16 h after install. #1867 (open) adds a run at install time |
| ⚠️ | **T+24 h**: two-way chat; the Planning Agent only delegates | Delegation works. The Planning Agent has no infrastructure tools but can comment on and unblock board cards and write memory; the restriction lives only in its config |

## 3. Proactive detection

| | Spec | Code today |
|---|---|---|
| ❌ | Deprecated APIs, found on a schedule before GKE upgrades | The scheduled job was retired; an on-demand scan checks manifests in Git only |
| ⚠️ | Over-requested CPU and memory against **14 days** of usage; opens pull requests | Weekly audit: 3 samples over ~**10 minutes**; flags ≤20% use with ≥2 vCPU or ≥4 GiB reclaimable. Pull requests only through `/remediate` |
| ✅ | Privileged containers | Daily compliance audit (`privileged: true`, SYS_ADMIN) |
| ✅ | cluster-admin bound to default service accounts | Daily audit flags any non-system account bound to cluster-admin (broader than the spec) |
| ⚠️ | Missing Workload Identity annotation or static keys | Daily check is cluster-wide only; the per-workload check runs once, at onboarding |
| ⚠️ | Single-replica workloads without a PDB | The PDB check needs **≥2** replicas; single-replica workloads get a separate minor finding |
| ➕ | Spot and Flex availability (spec: in development) | Already ships: daily 09:20 UTC, flags Spot preemption above 20%; Flex checked on request. No On-Demand plan in the repo |
| ⚠️ | Scale-up failures (FailedScaleUp, zone out of resources, quota) | On request only. The event watcher ignores FailedScaleUp; the stockout plugin is off by default |
| ⚠️ | ComputeClass advice for workloads pinned to one machine family | On request only; nothing detects pinned workloads |
| ❌ | Volumes above **85%** with a linear forecast | Not built |
| ⛔ | TLS certificates expiring within **7 days** | Not built; agents cannot read Secrets |
| ❌ | Image CVEs from Artifact Registry | Not built; the patch audit says "Never claim CVE coverage" |
| ➕ | Subnet IP exhaustion (spec: planned) | Already ships: daily 08:00 UTC, flags a range with less than 15% free |

## 4. Chat examples

| | Spec | Code today |
|---|---|---|
| ⚠️ | Why is a deployment failing readiness checks? | The troubleshooting skill has no readiness or probe step |
| ➕ | Spot/Flex availability and stockout risk (spec: planned) | Works (`capacity-obtainability`) |
| ✅ | Draft a ComputeClass pull request with Spot fallback | Design from `gke-compute-classes`, pull request through `submit-suggestion` |
| ⚠️ | Right-size limits from **7 days** of usage | ~10-minute sample; sets requests to 2× peak; leaves limits unchanged |
| ❌ | Who changed RBAC in the last 24 h? | No audit-log query for RBAC changes |
| ⚠️ | Will workloads break on a 1.30 → 1.31 upgrade? | Checks manifests in Git, not running workloads |
| ✅ | Any root or privileged pods in a namespace? | Covered by the compliance audit's checks |
| ⚠️ | Which nodes are under memory or CPU pressure? | `kubectl top nodes` usage only; no node-condition check |
| ❌ | Why does an Ingress return 502? | No troubleshooting content; backend health lookup not allowed |
| ❌ | Critical alerts across the fleet in 12 h, grouped by root cause | No time filter, no grouping |
| ⛔ | Validate a Workload Identity binding against GCP IAM | The service-account side of the binding cannot be read (IAM API blocked) |
| ✅ | Terraform change to enable Dataplane V2 (spec: planned) | Not built, as the spec says |

## 5. Architecture and lifecycle

| | Spec | Code today |
|---|---|---|
| ⛔ | MCP tools only, no raw shell commands | Agents have a terminal; `kubectl`, `gcloud`, `gh` and `git` run through the credential proxy, with the GKE MCP server alongside |
| ⚠️ | Envoy credential sidecars inject tokens | A separate proxy Deployment runs the commands itself; the sandbox holds no credentials; no token-rotation rules |
| ⚠️ | Installs into existing GKE clusters | Creates a new cluster by default; an existing cluster needs preparation steps |
| ❌ | Step-by-step root-cause reasoning defined in `SOUL.md` | Not described there |
| ❌ | Triage skill: trace cascading failures to one cause, silence the rest | No triage skill; duplicate alerts are merged only per pod and reason over 5 minutes (#660) |
| ❌ | Upgrades keep the persona, cron jobs and custom playbooks | `SOUL.md` and skills are overwritten from the image on every start; the image wins for every cron job it ships |
| ❌ | The agent refines its skills at runtime and keeps the changes | Edits are lost at the next restart |
| ❌ | Three-way merge of upstream and locally edited skills | The sync script wipes local edits and runs only before an image build |
| ❌ | MCP tool schemas checked at startup, mismatches posted to chat | Not built |
| ⛔ | Auto-approval of low-risk fixes (spec: planned) | The architecture spec says "there is no auto-merge for any tier" |
| ✅ | Skill regression tests | Exist as evals in `bench/tasks/` (47 cases), not in `tests/e2e/` |
| ✅ | Operator CRDs `kubeagents.x-k8s.io/v1alpha1` | Matches |
| ✅ | Read-only diagnostic access | Kubernetes get/list/watch; view-level GCP roles |
| ✅ | GKE hosted MCP endpoint | Loaded |
| ✅ | LiteLLM model gateway | Default |
| ✅ | Upgrades keep the data volume | Yes |

## ⛔ Existing repo decisions the spec would reverse

| Spec item | Decision it conflicts with |
|---|---|
| Nothing new while items are pending | `docs/designs/inventory-findings-queue.md` rejected rationing findings |
| TLS expiry check | Agents never get Secret access, and an admission policy blocks granting it |
| Workload Identity validation | The API policy refuses `iam.googleapis.com` |
| MCP only, no shell | The design gives agents a terminal whose commands the credential proxy runs |
| Auto-approval of low-risk fixes | The architecture spec says there is no auto-merge for any tier |

## In the code, not in the spec

- Alerts over the daily cap are dropped with no notice
- Findings reminder at 12:00 UTC every day
- Board-health post at 12:35 UTC every day
- One-time feedback prompt at 13:00 UTC, about 7 days after install
