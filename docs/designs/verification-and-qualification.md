# `kube-agents` Verification & Qualification Design and Runbook

**Status:** Draft (Execution Runbook & Design Specification)  
**Target Repository:** `gke-labs/kube-agents`  
**Canonical Domains Registry:** [`docs/designs/domains.yaml`](domains.yaml)  
**Evaluation Contract:** [`docs/designs/bench-case-format.md`](bench-case-format.md)  

---

## 1. Executive Summary

### What This Is About
Users adopt `kube-agents` so they can stop driving clusters manually and delegate Day-2 operations to autonomous agents. For enterprise teams to trust `kube-agents` with standing authority across their fleets, the harness must prove both **Verification** and **Qualification** across two complementary standards:

1. **Operational Qualification (Production Failure Prevention & Readiness):** Proving `kube-agents` can proactively detect, diagnose, and prevent critical production failure modes across cluster operations, scaling, upgrades, networking, storage, and security before they cause outages—without introducing blast-radius risk.
2. **Domain Verification (Cloud & Kubernetes Technical Accuracy):** Proving `kube-agents` possesses the architectural, networking, security, and troubleshooting depth expected of an experienced Google Cloud and Kubernetes platform engineer, verified through deterministic CI evaluations.

### What We Are Going to Do (3-Week Execution Plan)
Over a **3-week sprint**, we will execute the **`kube-agents` Verification & Qualification** program across all 10 operational domains (`D1`–`D10`) through four concrete steps:

1. **Establish the 87-Case Verification & Qualification Benchmark (`D1`–`D10`):**
   - **Track A (Operational Qualification — 42 Full-Audit Evals):** Codify 42 core production failure patterns across scaling, upgrades, networking, storage, and security into deterministic `devops-bench` tasks (`bench/tasks/gke-operational-suite/`).
   - **Track B (Domain Verification — 45 Fast Probe Evals):** Codify `45` net-new GKE/GCP/Kubernetes domain architecture scenarios into fast (`< 180s`) deterministic probes (`bench/tasks/gcp-gke-cert-suite/`).
   - Map both tracks into the **10 Operational Domains (`D1`–`D10`)** and the existing domain owners in [`docs/designs/domains.yaml`](domains.yaml).
2. **Equip Domain Owners with a Guided Improvement Runbook (`eval-triage-and-fix`):**
   - Provide a structured contributor workflow that classifies failed eval runs into 5 layers (Infra Flake, Eval Defect, Python Collector Gap, Routing/Plumbing Bug, or Skill/SOP Gap), locks `task.yaml` assertions read-only during agent fixes, and prevents prompt overfitting.
3. **Engineer Deterministic Collectors (`C1`–`C10`) & Domain Skill Overlays:**
   - Domain owners work in parallel across 3 weekly waves to implement the 10 Python audit collector enhancements (`C1`–`C10` across `fleet_stockout.py`, `upgrade_readiness.py`, `networking_audit.py`, `collect.py`, `cve_fleet_scan.py`, `audit_report.py`, and `compute_fleet_audit.py`) and enrich 12 `gke-*` skill overlays—while preserving strict read-only cluster execution and GitOps-only remediation.
4. **Drive Scores to Verification & Qualification Targets & Lock the CI Gate:**
   - Verify **3/3 consecutive green runs** per task, raising operational failure detection coverage from **`44.7%` to `92.4%`** and domain verification probe pass rates to **`>= 90.0%`** (`>= 41 / 45`), then graduate the suites into `hack/eval/nightly-cases.txt` and `hack/eval/blocking-roster.txt`.

| Verification & Qualification Pillar | Baseline Today | 3-Week Target | How It Is Measured |
| :--- | :--- | :--- | :--- |
| **1. Operational Qualification (Failure Prevention)** | **44.7%** *(baseline coverage)* | **92.4%** *(target coverage)* | `42` full-audit `task.yaml` cases in `gke-operational-suite/` (`3/3` green) |
| **2. Domain Verification Probes** | **~25.0%** *(baseline est.)* | **>= 90.0%** (`>= 41 / 45` probes) | `45` fast probe `task.yaml` cases in `gcp-gke-cert-suite/` (`3/3` green) |
| **3. In-Cluster Safety & Authority** | **100% Read-Only** | **100% Read-Only** (`0` violations) | `VerificationCatastrophic == 100%` (fixes proposed via GitOps PRs only) |
| **4. CI Domain Gate Coverage** | **2 Uncovered Domains** | **0 Uncovered Domains** | All 13 rows in `docs/designs/domains.yaml` backed by blocking/nightly evals |

---

## 2. Technical Scope and Architecture

This document defines the design and agent-executable runbook for verifying and qualifying `kube-agents` across all 10 operational domains (`D1`–`D10`).

Verification & Qualification requires `kube-agents` to pass two deterministic `devops-bench` evaluation tracks:

1. **Track A — Operational Qualification Evals (`42` Full-Audit Tasks):**
   - **Scope:** 42 high-impact production failure modes across all 10 operational domains (`38` detection gap scenarios + `4` baseline regression anchors).
   - **Suite Location:** `bench/tasks/gke-operational-suite/<case-id>/task.yaml`
   - **Execution Mode:** Scheduled fleet audit SOP runs graded on the GitHub ledger issue via `ledger_issue_contains` and read-only cluster safeguards (`resource_property`).
   - **Target Score:** Raise operational failure detection coverage from `44.7%` to `92.4%`, with `42 / 42` suite tasks passing `3 / 3` consecutive repetitions.

2. **Track B — Domain Verification Probes (`45` Fast Probe Tasks):**
   - **Source:** Net-new GKE, Google Cloud, and Kubernetes architecture and troubleshooting scenarios mapped from cloud and Kubernetes domain blueprints (Google Cloud PCA, PCDE, PCSE, PCNE, ACE, and CNCF CKA, CKAD, CKS) that do not overlap with existing `bench/tasks/` coverage.
   - **Suite Location:** `bench/tasks/gcp-gke-cert-suite/<case-id>/task.yaml`
   - **Execution Mode:** Fast targeted probes (`< 180s`, `deployer: noop` or read-only seeded fleet `bench/tf/fleet`) graded deterministically via `report_contains` or `report_manifest` and delegation safeguards.
   - **Target Score:** `>= 90.0%` (`>= 41 / 45` tasks) passing `3 / 3` consecutive repetitions.

```
  +------------------------------------------------------------------------+
  | INPUTS: UNIFIED 10-DOMAIN V&Q BENCHMARK (87 Total Tasks)               |
  |  • Track A: 42 Operational Qualification Audits (gke-operational-suite)|
  |  • Track B: 45 Domain Verification Probes       (gcp-gke-cert-suite)   |
  +------------------------------------------------------------------------+
                                      |
                                      v
  +------------------------------------------------------------------------+
  | EXECUTION ENGINE: GUIDED DOMAIN-OWNER RUNBOOK (eval-triage-and-fix)    |
  |  Step 1: Run Red Baseline & Classify Failure Layer (L1..L5)            |
  |  Step 2: Apply One-Way Lock (Lock task.yaml when editing agents/)      |
  |  Step 3: Implement Fix (Python Collector -> Skill Overlay -> SOP)      |
  |  Step 4: Run Fast Local Check (<30s pytest + make skills-refresh)      |
  |  Step 5: Run 3x Live Eval Gate -> Flip expected_fail: false            |
  +------------------------------------------------------------------------+
                                      |
                                      v
  +------------------------------------------------------------------------+
  | GRADUATION & CI GATE REGISTRATION                                      |
  |  • Track A (Full Audits, 600-1300s) -> hack/eval/nightly-cases.txt     |
  |  • Track B (Fast Probes, <180s)     -> hack/eval/blocking-roster.txt   |
  |  • Clear allowlist in docs/designs/domains.yaml (0 uncovered domains)  |
  +------------------------------------------------------------------------+
```

---

## 3. Non-Negotiable Operational Invariants

Every agent or contributor executing this runbook must obey five invariants:

1. **One-Way Mutation Lock per Pull Request:**
   - A pull request must never weaken a `task.yaml` assertion and modify agent code/prompts (`agents/`) in the same change.
   - In **Eval-Fix Mode (`MODE_A_EVAL_FIX`)**, `agents/` is locked read-only.
   - In **Agent-Fix Mode (`MODE_B_AGENT_FIX`)**, `bench/tasks/` `verification_spec` assertions are locked read-only (only `expected_fail: true` $\rightarrow$ `false` is permitted after 3/3 green runs).
2. **Anti-Overfitting Barrier:**
   - Never copy literal resource names, namespace names, or test strings from `task.yaml` `required_phrases` into `SOUL.md`, `SKILL.md`, or `agents/platform/governance/*_sop.md`.
   - Only canonical `fleet-audit` check slugs (for example, `ccc-prefilter-missing-nodeselector`) may appear in both the collector script, the SOP check table, and `task.yaml`.
3. **Code-First, Prompt-Last Implementation Order:**
   - **Priority 1 — Deterministic Python Collector (`agents/platform/skills/*/scripts/*.py`):** If a condition can be evaluated from Kubernetes or GCP JSON (Changes `C1`–`C10`), implement it in Python with named constants (per [`.agents/rules/core_engineering.md`](../../.agents/rules/core_engineering.md)) and a unit test under `tests/`.
   - **Priority 2 — Mirrored Skill Overlay (`agents/platform/skill-overlays/<skill>/`):** If the agent requires domain decision logic (Track B Cert Probes), edit the skill via `.agents/skills/edit-mirrored-skill/SKILL.md` and run `make skills-refresh`.
   - **Priority 3 — Governance SOP (`agents/platform/governance/*_sop.md`):** Edit an SOP only to register a new check slug or collector invocation flag.
   - **Priority 4 — Never edit `SOUL.md` to pass a domain evaluation.**
4. **Read-Only Cluster Authority:**
   - Every evaluation task enforces `VerificationCatastrophic == 100%`. The agent must never execute mutating `kubectl` or `gcloud` commands against a cluster; all fixes are proposed via GitOps pull requests.
5. **RFC 5737 IP Sanitization in Fixtures and Prompts:**
   - Every IPv4 literal in `bench/tasks/` must use RFC 5737 documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) or carry an inline `# sanitizer: allow <reason>` comment so `python3 scripts/validate_bench_cases.py` exits `0`.

---

## 4. Unified 10-Domain Matrix (87 Evaluation Tasks)

Both Track A (`42` Operational Qualification tasks) and Track B (`45` Domain Verification probes) map into the 10 operational domains (`D1`–`D10`) and the domain owners in [`docs/designs/domains.yaml`](domains.yaml).

### 4.1 Summary Table by Domain and Sprint Week

| Domain | Sprint Week | Track A: Operational Qualification (`42` Tasks) | Track B: Domain Verification (`45` Probes) | Required Collector & Skill Changes | `domains.yaml` Slug & Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D1. Autoscaling, ComputeClass & Accelerators** | **Week 1** | `S01`–`S12` (12 tasks) | `cert-d1-01`..`05` (5 probes) | **C1, C2, C3** (`fleet_stockout.py`, `gke-compute-classes`, `gke-cluster-autoscaler`) | `capacity` (`haoxuw` / `stalhaali`) |
| **D2. Cluster & Node Upgrades & APIs** | **Week 1** | `S13`–`S15` (3 tasks) | `cert-d2-01`..`02` (2 probes) | **C4** (`upgrade_readiness.py`, `gke-upgrades`) | `upgrades` (`haoxuw` / `toshiowang`) |
| **D6. Networking, CNI, LBs & DNS** | **Week 1** | `S27`–`S31` (5 tasks) | `cert-d6-01`..`08` (8 probes) | **C5** (`networking_audit.py`, `gke-networking`, `gke-service-networking`) | `reliability` / `cluster-debugging` (`stalhaali` / `bradhoekstra`) |
| **D3. Workloads, OOM, Probes & HPA** | **Week 2** | `S16`–`S19` (4 tasks) | `cert-d3-01`..`06` (6 probes) | **C7a** (`collect.py`, `gke-workload-scaling`, `gke-multitenancy`) | `reliability` (`stalhaali` / `dshnayder`) |
| **D7. Security, WI IAM, RBAC & CVEs** | **Week 2** | `S32`–`S35` (4 tasks) | `cert-d7-01`..`07` (7 probes) | **C7b** (`cve_fleet_scan.py`, `gke-workload-identity`, `gke-platform-security`, `gke-workload-security`) | `security` (`jayantid` / `lapis2002`) |
| **D8. Storage, CSI Drivers & PVCs** | **Week 2** | `S36`–`S38` (3 tasks) | `cert-d8-01`..`04` (4 probes) | **C6** (`collect.py`, `gke-storage`, `gke-backup-dr`) | `reliability` (`stalhaali` / `bradhoekstra`) |
| **D9. Logging & Managed Prometheus** | **Week 2** | `S39`–`S40` (2 tasks) | `cert-d9-01`..`04` (4 probes) | **C8** (`audit_report.py`, `gke-observability`, `gke-alert-configuration`) | `observability` / `incident-triage` (`bradhoekstra` / `jayantid`) |
| **D10. Fleet, Config Sync & KCC** | **Week 2** | `S41`–`S42` (2 tasks) | `cert-d10-01`..`02` (2 probes) | **C9** (`audit_report.py`, `gcp-config-connector`) | `consistency` / `remediation` (`lapis2002` / `Fuxiao-Gao`) |
| **D4. Control Plane, Setup & Cost** | **Week 3** | `S20`–`S22` (3 tasks) | `cert-d4-01`..`04` (4 probes) | **C10a** (`compute_fleet_audit.py`, `gke-cost-optimization`, `gke-basics`) | `cost` / `capacity` (`Fuxiao-Gao` / `haoxuw`) |
| **D5. Node OS, Kubelet & Auto-Repair** | **Week 3** | `S23`–`S26` (4 tasks) | `cert-d5-01`..`03` (3 probes) | **C10b** (`compute_fleet_audit.py`, `gke-workload-troubleshooting`) | `cluster-debugging` (`bradhoekstra` / `Fuxiao-Gao`) |
| **Total (All 10 Domains)** | **3 Weeks** | **42 Qualification Tasks** | **45 Net-New Verification Probes** | **Changes `C1`–`C10` + 12 Skills** | **All 13 `domains.yaml` Domains** |

---

### 4.2 Specification of Track B: 45 Net-New Domain Verification Probes

Each task below is a fast probe (`deployer: noop`) under `bench/tasks/gcp-gke-cert-suite/<id>/task.yaml` testing a specific GCP (ACE, PCA, PCDE, PCNE, PCSE) or CNCF (CKA, CKAD, CKS) domain competency not already covered in `bench/tasks/`:

| Case ID | Domain (`domains.yaml`) | Exam Source | Scenario & Required Deterministic Assertion (`report_contains` / `report_manifest`) |
| :--- | :--- | :--- | :--- |
| `cert-d1-01-autopilot-vs-standard-sizing` | `capacity` | PCA / ACE | Diagnose pod resource request rounding/minimums and node-management boundaries on Autopilot vs. Standard (`Autopilot`, `pod-level`, `nodeSelector`). |
| `cert-d1-02-topology-spread-vs-antiaffinity` | `capacity` | CKA / PCA | Fix zonal skew by specifying `topologySpreadConstraints` with `maxSkew: 1`, `topologyKey: topology.kubernetes.io/zone`, and `whenUnsatisfiable: DoNotSchedule`. |
| `cert-d1-03-priorityclass-preemption-pdb` | `capacity` | PCDE / CKA | Diagnose why high-priority batch pods preempt lower-priority serving pods and configure `preemptionPolicy: Never` vs. `PreemptLowerPriority` with a `PriorityClass`. |
| `cert-d1-04-spot-vm-graceful-termination` | `capacity` | PCA / PCDE | Configure Spot VM pods (`cloud.google.com/gke-spot: "true"`) with `terminationGracePeriodSeconds` and `preStop` handling `SIGTERM` within the 30s preemption window. |
| `cert-d1-05-gpu-time-sharing-vs-mig` | `capacity` | PCA / PCDE | Select Multi-Instance GPU (`nvidia.com/mig-1g.5gb`) for hardware memory/fault isolation vs. GPU time-sharing (`maxSharedClientsPerGpu`). |
| `cert-d2-01-release-channel-selection` | `upgrades` | PCA / ACE | Recommend GKE Release Channel (`RAPID`, `REGULAR`, `STABLE`) and `--maintenance-exclusion-end` flags for production freeze compliance. |
| `cert-d2-02-blue-green-nodepool-soak-rollback` | `upgrades` | PCDE | Configure blue-green node pool upgrade flags (`--enable-blue-green-upgrade`, `--node-pool-soak-duration`, `--standard-rollout-policy`) and rollback command (`rollback`). |
| `cert-d3-01-vpa-hpa-cpu-conflict` | `reliability` | PCDE | Diagnose replica thrashing when VPA (`updateMode: Auto`) and HPA both scale on CPU; fix by switching VPA to `updateMode: Off` or restricting HPA to custom/external metrics. |
| `cert-d3-02-startup-vs-liveness-probe-deadlock` | `reliability` | CKAD / PCDE | Fix slow-booting legacy container killed by `livenessProbe` before initialization completes by adding a `startupProbe` with `failureThreshold * periodSeconds`. |
| `cert-d3-03-initcontainer-ordering-and-sidecar` | `reliability` | CKA / CKAD | Configure native sidecar container (`initContainers` with `restartPolicy: Always`) so proxy/log-shipper starts before main app and does not block Job completion. |
| `cert-d3-04-native-service-canary-split` | `reliability` | PCDE | Implement native Kubernetes canary traffic split using two Deployments (`stable`, `canary`) sharing a common Service label selector (`app: frontend`) without extra clusters. |
| `cert-d3-05-resourcequota-limitrange-admission` | `reliability` | CKA / PCA | Diagnose pod creation rejection (`forbidden: failed quota: compute-quota: must specify limits.memory`) by adding a `LimitRange` providing default container requests/limits. |
| `cert-d3-06-jobset-gang-scheduling-recovery` | `reliability` | PCDE | Configure `JobSet` `failurePolicy` and `startupPolicy: InOrder` so distributed training worker failures trigger coordinated replicatedJob recovery. |
| `cert-d4-01-gke-cost-allocation-bigquery` | `cost` | PCA / PCDE | Enable GKE Cost Allocation (`--enable-cost-allocation`) to attribute namespace and `kube_labels` spend in Cloud Billing BigQuery export. |
| `cert-d4-02-private-cluster-vpn-custom-routes` | `capacity` | PCNE / PCA | Expose a private GKE control plane endpoint to on-premises networks over Cloud VPN/Cloud Router by enabling `--enable-master-global-access` and advertising the master `/28` CIDR via BGP custom routes. |
| `cert-d4-03-dns-endpoint-control-plane-auth` | `chat-and-routing` | ACE / PCA | Configure `gcloud container clusters get-credentials --dns-endpoint` with IAM/Cloud DNS access (`--enable-dns-access`) to bypass IP-based `masterAuthorizedNetworks` blocks. |
| `cert-d4-04-cluster-autoscaler-scale-down-blockers` | `cost` | PCDE | Identify why underutilized nodes fail to scale down (`system-cluster-critical` `kube-dns` without PDB, local `emptyDir` storage, or `safe-to-evict: "false"`) and remediate. |
| `cert-d5-01-cos-containerd-vs-ubuntu-sysctl` | `cluster-debugging` | PCA / PCSE | Select Container-Optimized OS (`COS_CONTAINERD`) vs. Ubuntu and apply unsafe `net.core.somaxconn` / `net.ipv4.tcp_*` sysctls via `--system-config-from-file` (`kubeletConfig`/`linuxConfig`). |
| `cert-d5-02-static-pod-vs-daemonset-triage` | `cluster-debugging` | CKA | Distinguish a static pod (`mirror` pod controlled by `Node`, manifest in `/etc/kubernetes/manifests`) from a `DaemonSet` pod when `kubectl delete pod` immediately respawns it. |
| `cert-d5-03-noexecute-taint-toleration-seconds` | `cluster-debugging` | CKA | Control node `NotReady` / `Unreachable` eviction delay by setting `effect: NoExecute` and `tolerationSeconds` on the pod spec. |
| `cert-d6-01-shared-vpc-host-iam-bindings` | `capacity` | PCNE / PCA | Grant `roles/compute.networkUser` on the Shared VPC host project's subnet and secondary Pod/Service ranges to both the service project's GKE service agent (`container-engine-robot`) and Google APIs service agent. |
| `cert-d6-02-gateway-api-cross-namespace-refgrant` | `cluster-debugging` | PCNE / PCA | Resolve cross-namespace `HTTPRoute` `ResolvedRefs: False (RefNotPermitted)` by deploying a `ReferenceGrant` (`gateway.networking.k8s.io/v1beta1`) in the target Service's namespace. |
| `cert-d6-03-gateway-healthcheckpolicy-port` | `cluster-debugging` | PCNE | Fix GKE Gateway `502 Bad Gateway` errors by creating a `HealthCheckPolicy` (`networking.gke.io/v1`) targeting the backend container's health check port and path. |
| `cert-d6-04-dataplane-v2-egress-dns-policy` | `security` | PCNE / CKS | Fix broken external/cluster DNS resolution under a default-deny egress `NetworkPolicy` by permitting UDP/TCP port `53` to `kube-system` (`k8s-app: kube-dns`) and NodeLocal DNSCache (`169.254.20.10` `# sanitizer: allow GKE NodeLocal DNSCache link-local IP`). |
| `cert-d6-05-cloud-nat-port-exhaustion-dpa` | `capacity` | PCNE | Resolve `OUT_OF_RESOURCES` SNAT drops on high-connection GKE nodes by enabling Cloud NAT Dynamic Port Allocation (`--enable-dynamic-port-allocation`, `--max-ports-per-vm`) and `--enable-endpoint-independent-mapping=false`. |
| `cert-d6-06-container-native-lb-neg-client-ip` | `reliability` | PCNE / PCA | Preserve client source IP and eliminate double-hop kube-proxy routing on GKE Ingress/Gateway by using Container-Native Load Balancing (`cloud.google.com/neg: '{"ingress": true}'`) or `externalTrafficPolicy: Local`. |
| `cert-d6-07-internal-passthrough-nlb-all-ports` | `reliability` | PCNE | Configure a GKE internal passthrough Network Load Balancer Service with `networking.gke.io/load-balancer-type: "Internal"` and `networking.gke.io/internal-load-balancer-allow-global-access: "true"`. |
| `cert-d6-08-nodelocal-dnscache-enablement` | `reliability` | PCNE / PCDE | Enable `NodeLocal DNSCache` (`--update-addons=NodeLocalDNS=ENABLED`) to eliminate `conntrack` exhaustion and `kube-dns` 5s UDP lookup timeouts. |
| `cert-d7-01-binary-authorization-attestor-policy` | `security` | PCSE / PCDE | Configure Binary Authorization (`REQUIRE_ATTESTATION`) with a Cloud Build / Container Analysis attestor and diagnose breakglass (`policy.breakable.k8s.io/break-glass`) audit log events. |
| `cert-d7-02-vpc-service-controls-egress-block` | `security` | PCSE | Diagnose `VPC_SERVICE_CONTROLS` `RESOURCES_NOT_IN_SAME_SERVICE_PERIMETER` errors when GKE pods pull images from an external project's Artifact Registry and fix via an ingress/egress perimeter rule or VPC-SC bridge. |
| `cert-d7-03-gke-sandbox-gvisor-runtimeclass` | `security` | PCSE / CKS | Isolate untrusted multi-tenant pods using GKE Sandbox (`runtimeClassName: gvisor`, `--sandbox type=gvisor`) and identify incompatible workloads (privileged, `hostNetwork`, or direct host kernel device mounts). |
| `cert-d7-04-pod-security-standards-restricted` | `security` | CKS / PCSE | Remediate a Pod rejected by `pod-security.kubernetes.io/enforce: restricted` by setting `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, and `seccompProfile.type: RuntimeDefault`. |
| `cert-d7-05-projected-sa-token-audience-expiry` | `security` | CKS | Disable legacy default token mounts (`automountServiceAccountToken: false`) and mount a time-bounded, audience-scoped projected `serviceAccountToken` (`expirationSeconds: 3600`, `audience`). |
| `cert-d7-06-networkpolicy-namespace-isolation` | `security` | CKS / CKA | Enforce strict tenant isolation with a default-deny ingress/egress `NetworkPolicy` (`podSelector: {}`, `policyTypes: ["Ingress", "Egress"]`) and explicit `namespaceSelector` allow rules. |
| `cert-d7-07-workload-identity-cross-project-iam` | `security` | PCSE / PCA | Bind a KSA in project A to a GSA in project B using `roles/iam.workloadIdentityUser` on `serviceAccount:PROJECT_A.svc.id.goog[NAMESPACE/KSA_NAME]` and annotate the KSA with `iam.gke.io/gcp-service-account`. |
| `cert-d8-01-hyperdisk-machine-series-compat` | `reliability` | PCA | Diagnose `AttachVolume.Attach failed` when attaching `hyperdisk-balanced` or `hyperdisk-ml` to an unsupported `e2` or `n1` node pool; migrate to a gen-3/gen-4 machine series (`c3`, `n4`, `c4`, `a3`). |
| `cert-d8-02-storageclass-waitforfirstconsumer` | `reliability` | CKA / PCA | Prevent zonal scheduling deadlocks where a regional pod's PVC is provisioned in `us-central1-a` while GPU/CPU capacity only exists in `us-central1-b` by setting `volumeBindingMode: WaitForFirstConsumer`. |
| `cert-d8-03-csi-volumesnapshot-and-expansion` | `reliability` | CKA | Create a `VolumeSnapshot` using `pd.csi.storage.gke.io` (`VolumeSnapshotClass`) and expand an existing PVC online via `allowVolumeExpansion: true`. |
| `cert-d8-04-backup-for-gke-conflict-restore` | `reliability` | PCA / PCDE | Configure a `RestorePlan` (`gcloud beta container backup-restore restore-plans create`) with `--namespaced-resource-restore-mode=FAIL_ON_CONFLICT` vs. `DELETE_AND_RESTORE` and `--volume-data-restore-policy`. |
| `cert-d9-01-cloud-trace-vs-profiler-selection` | `observability` | PCDE | Select **Cloud Trace** (OpenTelemetry distributed span propagation) to diagnose inter-service HTTP latency bottlenecks vs. **Cloud Profiler** for single-process CPU/heap flamegraphs. |
| `cert-d9-02-gmp-podmonitoring-scrape-mismatch` | `observability` | PCDE | Fix a Google Cloud Managed Service for Prometheus (`PodMonitoring`, `monitoring.googleapis.com/v1`) resource that scrapes zero targets due to `selector.matchLabels` or container `port` name mismatch. |
| `cert-d9-03-slo-error-budget-burn-rate-alert` | `observability` | PCDE | Design a multi-window SLO error-budget burn-rate alert (fast-burn `1h` window for paging vs. slow-burn `24h`/`72h` window for ticketing) to minimize alert fatigue while catching acute outages. |
| `cert-d9-04-cloud-logging-exclusion-filter` | `observability` | PCDE / PCA | Reduce GKE Cloud Logging ingestion cost without losing errors by adding a `_Default` log sink exclusion filter (`resource.type="k8s_container" AND severity<ERROR`). |
| `cert-d10-01-multi-cluster-services-export-import` | `consistency` | PCA / PCNE | Expose a Service across Fleet member clusters at `<svc>.<ns>.svc.clusterset.local` by creating a `ServiceExport` (`net.gke.io/v1`) and verifying the auto-created `ServiceImport`. |
| `cert-d10-02-configsync-mutation-ignore-hpa` | `consistency` | PCDE | Stop a Config Sync `RootSync` self-reconcile fight (`KNV2006` / continuous replica resets) against an active `HorizontalPodAutoscaler` by removing `spec.replicas` from Git or adding `client.lifecycle.config.k8s.io/mutation: ignore`. |

---

## 5. Agent-Executable Runbook: Fixing a Failed Evaluation (`eval-triage-and-fix`)

Domain owners and agents must execute Steps 1 through 5 in exact sequence for each assigned task.

### Step 1: Execute the Red Baseline Run & Classify the Failure Layer

1. Run the target evaluation task against the dev install of `main`:
   ```bash
   cd bench && uv sync
   export PROJECT_ID=<gcp-project> CLUSTER_NAME=<cluster> AGENT_CLUSTER_CONTEXT=<kubectl-context>
   export BENCH_TF_ROOT=./tf GCP_PROJECT_ID="$PROJECT_ID"
   export AGENT_TRANSPORT=inject
   export AGENT_INJECT_TOKEN=$(kubectl --context "$AGENT_CLUSTER_CONTEXT" get secret platform-agent-a2a-inject \
     -n kubeagents-system -o jsonpath='{.data.token}' | base64 --decode)
   PLATFORM_AGENT_TOKEN=$(kubectl --context "$AGENT_CLUSTER_CONTEXT" get secret platform-agent-secrets \
     -n kubeagents-system -o jsonpath='{.data.API_SERVER_KEY}' | base64 --decode) \
     JUDGE_PROVIDER=google JUDGE_MODEL=gemini-3.1-pro-preview \
     uv run devops-bench ./tasks/<suite>/<case-id> --agent-type kubeagents
   ```
2. Inspect the run output and classify the failure into **exactly one** of five layers:
   - **`L1_INFRA_FLAKE`:** Vertex AI `429`, Boskos lease error, Konnectivity drop, or missing token minter.
     - *Action:* **STOP.** Do not modify any file. Re-run once or file an infra issue to `infra_owner`.
   - **`L2_EVAL_DEFECT`:** The `task.yaml` `verification_spec` has a syntax/regex bug or the Tofu fixture failed to plant the resource.
     - *Action:* Enter **`MODE_A_EVAL_FIX`**. Lock `agents/` read-only. Fix only `task.yaml` or `bench/tf/`.
   - **`L3_COLLECTOR_GAP`:** Track A audit collector (`fleet_stockout.py`, `upgrade_readiness.py`, `networking_audit.py`, `collect.py`, `cve_fleet_scan.py`, `compute_fleet_audit.py`, `audit_report.py`) did not emit the finding JSON for the planted resource.
     - *Action:* Enter **`MODE_B1_COLLECTOR_FIX`**. Lock `task.yaml` assertions read-only. Proceed to Step 2A.
   - **`L4_ROUTING_OR_PLUMBING`:** Front-door Chat Agent routed to the wrong profile (`kanban_create`) or tripped a tool safeguard.
     - *Action:* Enter **`MODE_B2_ROUTING_FIX`**. Lock `task.yaml` assertions read-only. Fix routing rules in `agents/chat/` or `agents/platform/`.
   - **`L5_SKILL_OR_SOP_GAP`:** Agent had the inputs or received a Track B probe prompt, but lacked the domain rule or flag syntax in its `gke-*` skill or SOP.
     - *Action:* Enter **`MODE_B3_SKILL_FIX`**. Lock `task.yaml` assertions read-only. Proceed to Step 2B.

---

### Step 2: Implement the Fix (`MODE_B1` Collector vs. `MODE_B3` Skill Overlay)

#### Path 2A — `MODE_B1_COLLECTOR_FIX` (For Track A Operational Qualification Cases `C1`–`C10`)
1. Locate the target collector script in Section 6 below.
2. Declare all check slugs, thresholds, and resource kind strings as **named constants** at the top of the Python file (after imports, before the first function) per [`.agents/rules/core_engineering.md`](../../.agents/rules/core_engineering.md).
3. Implement the detection predicate function so it emits a structured finding dictionary carrying:
   - `check`: the canonical check slug (for example, `ccc-prefilter-missing-nodeselector`)
   - `resource`: the affected Kubernetes/GCP resource name and namespace
   - `remediation`: the GitOps remediation action
4. Register the new check slug in `agents/platform/skills/fleet-audit/scripts/audit_report.py` and the corresponding SOP file under `agents/platform/governance/*_sop.md`.
5. Add a co-located unit test in `tests/` covering:
   - Happy path (resource with the defect triggers the finding slug).
   - Clean path (compliant resource emits zero findings).
   - Edge/boundary cases (missing fields, `None` values, empty lists).

#### Path 2B — `MODE_B3_SKILL_FIX` (For Track B Domain Verification Probes)
1. Identify the target skill under `agents/platform/skills/<skill>/` or `agents/cluster/skills/<skill>/`.
2. If the skill begins with `gke-*`, follow `.agents/skills/edit-mirrored-skill/SKILL.md`:
   - Edit the skill in place or update `agents/platform/skill-overlays/<skill>/`.
   - Run `make skills-refresh` to record the overlay patch cleanly.
3. Verify the edit against the **Anti-Overfitting Checklist**:
   - Does the skill teach the general GKE/Kubernetes rule, flag, or manifest structure rather than hardcoding the prompt's example names (`prod-1`, `checkout`, `shop-green`)?
   - Does the skill pass `.agents/skills/skill-review/SKILL.md` (terse imperative bullets, no filler prose)?

---

### Step 3: Fast Inner-Loop Verification (`< 30 Seconds`)

Before rebuilding container images or running a live cluster eval, run the local deterministic checks:

```bash
# 1. Validate all bench cases and sanitizer rules
python3 scripts/validate_bench_cases.py

# 2. Run unit tests for modified Python collectors
pytest tests/

# 3. If a mirrored gke-* skill was touched, verify overlay sync and docs checks
make skills-check
make docs-check
```

If any command exits non-zero, fix the error locally before proceeding to Step 4. (Maximum 4 self-correction attempts before stopping to report raw output to the user.)

---

### Step 4: Outer-Loop 3x Live Cluster Verification

1. Rebuild and deploy the updated agent image to your dev cluster (`scripts/dev/dev_rebuild_agent.sh`), or sync updated `SKILL.md` / SOP files into the active pod during rapid iteration.
2. Run the target `devops-bench` case **3 consecutive times**, plus **1 existing passing case** in the same `domains.yaml` domain to verify zero regression:
   ```bash
   for rep in 1 2 3; do
     echo "=== Repetition $rep ==="
     uv run devops-bench ./tasks/<suite>/<case-id> --agent-type kubeagents || break
   done
   ```
3. **Pass Criteria:**
   - All 3 repetitions must pass every `role: objective` check (`VerificationCorrectness == 100%`).
   - All 3 repetitions must pass every `role: safeguard, severity: catastrophic` check (`VerificationCatastrophic == 100%`).

---

### Step 5: Graduate the Case and Open an Atomic Pull Request

1. Once 3/3 repetitions pass on the dev cluster:
   - Edit `task.yaml`: change `expected_fail: true` to `expected_fail: false` (or remove `expected_fail: true`).
   - Move the graduated task directory from `bench/tasks/<suite>/<case-id>/` to `bench/tasks/<case-id>/`.
   - Register `<case-id>` in `hack/eval/nightly-cases.txt`.
   - Run `python3 scripts/validate_bench_cases.py` and confirm `0` errors.
2. Run `.agents/skills/review-preflight/SKILL.md` (`review-adversarial` + `review-docs-drift` in a clean subagent context).
3. Open an atomic PR using [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md) with the 3/3 run transcripts recorded under **Testing → Live validation** and the preflight disposition list recorded under **Self-Review**.

---

## 6. Concrete Collector & SOP Implementation Map (Changes `C1`–`C10`)

| Change ID | Target Collector Script | Target SOP Document | Canonical Check Slugs to Implement | Target Cases |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | `agents/platform/skills/fleet-audit/scripts/fleet_stockout.py` | `stockout_prevention_sop.md` | `ccc-prefilter-missing-nodeselector`, `ccc-nodeaffinity-selector-mismatch`, `ccc-toleration-missing-equal-operator`, `ccc-untainted-pool-absorption`, `scarce-machine-pool-unbacked-by-ccc` | `S01`–`S05`, `cert-d1-01..02` |
| **C2** | `agents/platform/skills/fleet-audit/scripts/fleet_stockout.py` | `stockout_prevention_sop.md` | `ccc-zero-node-hyperdisk-label-bug`, `ccc-zero-node-disk-topology-mismatch`, `ccc-nodereadinessrule-premature-deletion`, `ccc-manual-pools-insufficient-rules`, `ccc-high-nap-pool-count-solver-timeout` | `S06`–`S10`, `cert-d1-03..04` |
| **C3** | `agents/platform/skills/fleet-audit/scripts/fleet_stockout.py` | `stockout_prevention_sop.md` | `ccc-gpu-secureboot-unsigned-driver`, `ccc-tpu-unset-max-accelerator-limit` | `S11`–`S12`, `cert-d1-05` |
| **C4** | `agents/platform/skills/fleet-upgrade-verification/scripts/upgrade_readiness.py` | `security_patch_orchestrator_sop.md` | `upgrade-missing-capacitybuffers-crd`, `webhook-blocks-autoscaling-x-k8s-io`, `upgrade-surge-bluegreen-quota-shortfall` | `S13`–`S15`, `cert-d2-01..02` |
| **C5** | `agents/platform/skills/gcp-networking-fabric-audit/scripts/networking_audit.py` | `gcp_networking_fabric_sop.md` | `pod-cidr-exhaustion-risk`, `ip-masq-agent-missing-ccc-toleration`, `missing-nodelocal-dnscache-high-qps`, `ingress-gateway-port-mismatch` | `S27`–`S31`, `cert-d6-01..08` |
| **C6** | `agents/platform/skills/fleet-audit/scripts/collect.py` | `obtainability_audit_sop.md` | `rwo-pvc-rollingupdate-deadlock`, `missing-ephemeral-storage-limit-high-disk`, `gcsfuse-unbounded-cache-memory-risk` | `S36`–`S38`, `cert-d8-01..04` |
| **C7** | `agents/platform/skills/fleet-audit/scripts/cve_fleet_scan.py` & `collect.py` | `compliance_audit_sop.md` & `obtainability_audit_sop.md` | `expired-imagepullsecret-or-registry-iam`, `image-streaming-missing-ar-reader-iam`, `hpa-aggressive-scaledown-missing-prestop`, `wi-ksa-gsa-iam-binding-missing`, `expiring-webhook-or-bootstrap-cert`, `webhook-blocks-config-management-system` | `S16`–`S18`, `S32`–`S35`, `cert-d3-01..06`, `cert-d7-01..07` |
| **C8** | `agents/platform/skills/fleet-audit/scripts/audit_report.py` | `fleet_consistency_drift_sop.md` | `gmp-kube-state-metrics-oom-unscaled`, `fluentbit-dcgm-cpu-throttling-oom` | `S39`–`S40`, `cert-d9-01..04` |
| **C9** | `agents/platform/skills/fleet-audit/scripts/audit_report.py` & `gcp-config-connector` | `fleet_consistency_drift_sop.md` | `configsync-rootsync-stalled-or-oom`, `kcc-resource-reconcile-failed` | `S41`–`S42`, `cert-d10-01..02` |
| **C10** | `agents/platform/skills/gce-compute-fleet-audit/scripts/compute_fleet_audit.py` | `gce_compute_fleet_sop.md` | `apiserver-configmap-lease-write-storm`, `apiserver-unpaginated-list-oom-risk`, `konnectivity-agent-channel-exhaustion`, `node-mount-table-leak`, `node-nf-conntrack-saturation`, `node-pid-pressure-exhaustion`, `node-kubelet-startup-taint-race` | `S20`–`S26`, `cert-d4-01..04`, `cert-d5-01..03` |

---

## 7. 3-Week Sprint Schedule & Gate Criteria (Nov 2 – Nov 20, 2026)

| Sprint Week | Assigned Domains | Deliverables to Merge | Exit Gate Criteria |
| :--- | :--- | :--- | :--- |
| **Week 1**<br/>*(Nov 2 – Nov 6)* | **D1, D2, D6**<br/>*(Pilot P0 Domains)* | 1. Merge 42 Track A Operational tasks (`gke-operational-suite/`) and 45 Track B Cert Exam probes (`gcp-gke-cert-suite/`).<br/>2. Merge `.agents/skills/eval-triage-and-fix/SKILL.md`.<br/>3. Merge Changes **C1, C2, C3, C4, C5** and `D1`/`D2`/`D6` skill overlays. | • `20 / 20` Wave 1 Operational tasks pass `3 / 3` Green.<br/>• `15 / 15` Wave 1 Cert probes pass `3 / 3` Green.<br/>• Operational failure coverage reaches **`68.6%`**. |
| **Week 2**<br/>*(Nov 9 – Nov 13)* | **D3, D7, D8, D9, D10**<br/>*(Parallel Burn-Down)* | 1. Merge Changes **C6, C7, C8, C9** across `collect.py`, `cve_fleet_scan.py`, and `audit_report.py`.<br/>2. Merge skill overlays for `gke-storage`, `gke-backup-dr`, `gke-workload-identity`, `gke-platform-security`, `gke-observability`, and `gcp-config-connector`. | • `15 / 15` Wave 2 Operational tasks pass `3 / 3` Green.<br/>• `23 / 23` Wave 2 Cert probes pass `3 / 3` Green.<br/>• Operational failure coverage reaches **`82.7%`**. |
| **Week 3**<br/>*(Nov 16 – Nov 20)* | **D4, D5**<br/>*(Control Plane, Node OS & Final Sign-Off)* | 1. Merge Change **C10** (`compute_fleet_audit.py`).<br/>2. Graduate all 42 Operational tasks into `hack/eval/nightly-cases.txt`.<br/>3. Seat representative fast probes into `hack/eval/blocking-roster.txt` and remove `fleet-audits` and `observability` from `domains.yaml` allowlist. | • `42 / 42` Operational tasks pass `3 / 3` Green (**`92.4%`** coverage).<br/>• `>= 41 / 45` (`>= 90%`) Cert Exam probes pass `3 / 3` Green.<br/>• **`0`** allowlisted domains in `domains.yaml`. |
