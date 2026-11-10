# GCP, GKE & Kubernetes Certification Exam Domain Evaluation Suite (45 Probes)

This evaluation suite defines **45 net-new `devops-bench` certification probes** (`bench/tasks/gcp-gke-cert-suite/<case-id>/task.yaml`) mapped across all 10 GKE operational domains (`D1`–`D10`) and [`docs/designs/domains.yaml`](../../docs/designs/domains.yaml).

## Summary Matrix of All 45 Certification Exam Probes

| # | Task Case ID | GKE Operational Domain | `domains.yaml` | Exam Source | Target Skill |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C01 | [`cert-d1-01-autopilot-vs-standard-sizing`](gcp-gke-cert-suite/cert-d1-01-autopilot-vs-standard-sizing/task.yaml) | D1. Autoscaling, ComputeClass & Accelerators | `capacity` | GCP PCA / ACE | `gke-compute-classes` |
| C02 | [`cert-d1-02-topology-spread-vs-antiaffinity`](gcp-gke-cert-suite/cert-d1-02-topology-spread-vs-antiaffinity/task.yaml) | D1. Autoscaling, ComputeClass & Accelerators | `capacity` | CNCF CKA / GCP PCA | `gke-workload-scaling` |
| C03 | [`cert-d1-03-priorityclass-preemption-pdb`](gcp-gke-cert-suite/cert-d1-03-priorityclass-preemption-pdb/task.yaml) | D1. Autoscaling, ComputeClass & Accelerators | `capacity` | GCP PCDE / CNCF CKA | `gke-workload-scaling` |
| C04 | [`cert-d1-04-spot-vm-graceful-termination`](gcp-gke-cert-suite/cert-d1-04-spot-vm-graceful-termination/task.yaml) | D1. Autoscaling, ComputeClass & Accelerators | `capacity` | GCP PCA / PCDE | `gke-compute-classes` |
| C05 | [`cert-d1-05-gpu-time-sharing-vs-mig`](gcp-gke-cert-suite/cert-d1-05-gpu-time-sharing-vs-mig/task.yaml) | D1. Autoscaling, ComputeClass & Accelerators | `capacity` | GCP PCA / PCDE | `gke-batch-hpc` |
| C06 | [`cert-d2-01-release-channel-selection`](gcp-gke-cert-suite/cert-d2-01-release-channel-selection/task.yaml) | D2. Cluster & Node Upgrades & APIs | `upgrades` | GCP PCA / ACE | `gke-upgrades` |
| C07 | [`cert-d2-02-blue-green-nodepool-soak-rollback`](gcp-gke-cert-suite/cert-d2-02-blue-green-nodepool-soak-rollback/task.yaml) | D2. Cluster & Node Upgrades & APIs | `upgrades` | GCP PCDE | `gke-upgrades` |
| C08 | [`cert-d3-01-vpa-hpa-cpu-conflict`](gcp-gke-cert-suite/cert-d3-01-vpa-hpa-cpu-conflict/task.yaml) | D3. Workloads, OOM, Probes & HPA | `reliability` | GCP PCDE | `gke-workload-scaling` |
| C09 | [`cert-d3-02-startup-vs-liveness-probe-deadlock`](gcp-gke-cert-suite/cert-d3-02-startup-vs-liveness-probe-deadlock/task.yaml) | D3. Workloads, OOM, Probes & HPA | `reliability` | CNCF CKAD / GCP PCDE | `gke-reliability` |
| C10 | [`cert-d3-03-initcontainer-ordering-and-sidecar`](gcp-gke-cert-suite/cert-d3-03-initcontainer-ordering-and-sidecar/task.yaml) | D3. Workloads, OOM, Probes & HPA | `reliability` | CNCF CKA / CKAD | `gke-reliability` |
| C11 | [`cert-d3-04-native-service-canary-split`](gcp-gke-cert-suite/cert-d3-04-native-service-canary-split/task.yaml) | D3. Workloads, OOM, Probes & HPA | `reliability` | GCP PCDE | `gke-service-networking` |
| C12 | [`cert-d3-05-resourcequota-limitrange-admission`](gcp-gke-cert-suite/cert-d3-05-resourcequota-limitrange-admission/task.yaml) | D3. Workloads, OOM, Probes & HPA | `reliability` | CNCF CKA / GCP PCA | `gke-multitenancy` |
| C13 | [`cert-d3-06-jobset-gang-scheduling-recovery`](gcp-gke-cert-suite/cert-d3-06-jobset-gang-scheduling-recovery/task.yaml) | D3. Workloads, OOM, Probes & HPA | `reliability` | GCP PCDE | `gke-ai-troubleshooting-jobset-interruption` |
| C14 | [`cert-d4-01-gke-cost-allocation-bigquery`](gcp-gke-cert-suite/cert-d4-01-gke-cost-allocation-bigquery/task.yaml) | D4. Control Plane, Setup, Cost & CLI | `cost` | GCP PCA / PCDE | `gke-cost-analysis` |
| C15 | [`cert-d4-02-private-cluster-vpn-custom-routes`](gcp-gke-cert-suite/cert-d4-02-private-cluster-vpn-custom-routes/task.yaml) | D4. Control Plane, Setup, Cost & CLI | `capacity` | GCP PCNE / PCA | `gke-networking` |
| C16 | [`cert-d4-03-dns-endpoint-control-plane-auth`](gcp-gke-cert-suite/cert-d4-03-dns-endpoint-control-plane-auth/task.yaml) | D4. Control Plane, Setup, Cost & CLI | `chat-and-routing` | GCP ACE / PCA | `gke-basics` |
| C17 | [`cert-d4-04-cluster-autoscaler-scale-down-blockers`](gcp-gke-cert-suite/cert-d4-04-cluster-autoscaler-scale-down-blockers/task.yaml) | D4. Control Plane, Setup, Cost & CLI | `cost` | GCP PCDE | `gke-cluster-autoscaler` |
| C18 | [`cert-d5-01-cos-containerd-vs-ubuntu-sysctl`](gcp-gke-cert-suite/cert-d5-01-cos-containerd-vs-ubuntu-sysctl/task.yaml) | D5. Node OS, Kubelet & Auto-Repair | `cluster-debugging` | GCP PCA / PCSE | `gke-workload-troubleshooting` |
| C19 | [`cert-d5-02-static-pod-vs-daemonset-triage`](gcp-gke-cert-suite/cert-d5-02-static-pod-vs-daemonset-triage/task.yaml) | D5. Node OS, Kubelet & Auto-Repair | `cluster-debugging` | CNCF CKA | `gke-workload-troubleshooting` |
| C20 | [`cert-d5-03-noexecute-taint-toleration-seconds`](gcp-gke-cert-suite/cert-d5-03-noexecute-taint-toleration-seconds/task.yaml) | D5. Node OS, Kubelet & Auto-Repair | `cluster-debugging` | CNCF CKA | `gke-reliability` |
| C21 | [`cert-d6-01-shared-vpc-host-iam-bindings`](gcp-gke-cert-suite/cert-d6-01-shared-vpc-host-iam-bindings/task.yaml) | D6. Networking, CNI, LBs & DNS | `capacity` | GCP PCNE / PCA | `gke-networking` |
| C22 | [`cert-d6-02-gateway-api-cross-namespace-refgrant`](gcp-gke-cert-suite/cert-d6-02-gateway-api-cross-namespace-refgrant/task.yaml) | D6. Networking, CNI, LBs & DNS | `cluster-debugging` | GCP PCNE / PCA | `gke-service-networking` |
| C23 | [`cert-d6-03-gateway-healthcheckpolicy-port`](gcp-gke-cert-suite/cert-d6-03-gateway-healthcheckpolicy-port/task.yaml) | D6. Networking, CNI, LBs & DNS | `cluster-debugging` | GCP PCNE | `gke-service-networking` |
| C24 | [`cert-d6-04-dataplane-v2-egress-dns-policy`](gcp-gke-cert-suite/cert-d6-04-dataplane-v2-egress-dns-policy/task.yaml) | D6. Networking, CNI, LBs & DNS | `security` | GCP PCNE / CNCF CKS | `gke-networking` |
| C25 | [`cert-d6-05-cloud-nat-port-exhaustion-dpa`](gcp-gke-cert-suite/cert-d6-05-cloud-nat-port-exhaustion-dpa/task.yaml) | D6. Networking, CNI, LBs & DNS | `capacity` | GCP PCNE | `gke-networking` |
| C26 | [`cert-d6-06-container-native-lb-neg-client-ip`](gcp-gke-cert-suite/cert-d6-06-container-native-lb-neg-client-ip/task.yaml) | D6. Networking, CNI, LBs & DNS | `reliability` | GCP PCNE / PCA | `gke-service-networking` |
| C27 | [`cert-d6-07-internal-passthrough-nlb-all-ports`](gcp-gke-cert-suite/cert-d6-07-internal-passthrough-nlb-all-ports/task.yaml) | D6. Networking, CNI, LBs & DNS | `reliability` | GCP PCNE | `gke-service-networking` |
| C28 | [`cert-d6-08-nodelocal-dnscache-enablement`](gcp-gke-cert-suite/cert-d6-08-nodelocal-dnscache-enablement/task.yaml) | D6. Networking, CNI, LBs & DNS | `reliability` | GCP PCNE / PCDE | `gke-networking` |
| C29 | [`cert-d7-01-binary-authorization-attestor-policy`](gcp-gke-cert-suite/cert-d7-01-binary-authorization-attestor-policy/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | GCP PCSE / PCDE | `gke-platform-security` |
| C30 | [`cert-d7-02-vpc-service-controls-egress-block`](gcp-gke-cert-suite/cert-d7-02-vpc-service-controls-egress-block/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | GCP PCSE | `gke-platform-security` |
| C31 | [`cert-d7-03-gke-sandbox-gvisor-runtimeclass`](gcp-gke-cert-suite/cert-d7-03-gke-sandbox-gvisor-runtimeclass/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | GCP PCSE / CNCF CKS | `gke-workload-security` |
| C32 | [`cert-d7-04-pod-security-standards-restricted`](gcp-gke-cert-suite/cert-d7-04-pod-security-standards-restricted/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | CNCF CKS / GCP PCSE | `gke-workload-security` |
| C33 | [`cert-d7-05-projected-sa-token-audience-expiry`](gcp-gke-cert-suite/cert-d7-05-projected-sa-token-audience-expiry/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | CNCF CKS | `gke-workload-security` |
| C34 | [`cert-d7-06-networkpolicy-namespace-isolation`](gcp-gke-cert-suite/cert-d7-06-networkpolicy-namespace-isolation/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | CNCF CKS / CKA | `gke-networking` |
| C35 | [`cert-d7-07-workload-identity-cross-project-iam`](gcp-gke-cert-suite/cert-d7-07-workload-identity-cross-project-iam/task.yaml) | D7. Security, WI IAM, RBAC & CVEs | `security` | GCP PCSE / PCA | `gke-workload-identity` |
| C36 | [`cert-d8-01-hyperdisk-machine-series-compat`](gcp-gke-cert-suite/cert-d8-01-hyperdisk-machine-series-compat/task.yaml) | D8. Storage, CSI Drivers & PVCs | `reliability` | GCP PCA | `gke-storage` |
| C37 | [`cert-d8-02-storageclass-waitforfirstconsumer`](gcp-gke-cert-suite/cert-d8-02-storageclass-waitforfirstconsumer/task.yaml) | D8. Storage, CSI Drivers & PVCs | `reliability` | CNCF CKA / GCP PCA | `gke-storage` |
| C38 | [`cert-d8-03-csi-volumesnapshot-and-expansion`](gcp-gke-cert-suite/cert-d8-03-csi-volumesnapshot-and-expansion/task.yaml) | D8. Storage, CSI Drivers & PVCs | `reliability` | CNCF CKA | `gke-storage` |
| C39 | [`cert-d8-04-backup-for-gke-conflict-restore`](gcp-gke-cert-suite/cert-d8-04-backup-for-gke-conflict-restore/task.yaml) | D8. Storage, CSI Drivers & PVCs | `reliability` | GCP PCA / PCDE | `gke-backup-dr` |
| C40 | [`cert-d9-01-cloud-trace-vs-profiler-selection`](gcp-gke-cert-suite/cert-d9-01-cloud-trace-vs-profiler-selection/task.yaml) | D9. Logging (FluentBit) & Managed Prometheus | `observability` | GCP PCDE | `gke-observability` |
| C41 | [`cert-d9-02-gmp-podmonitoring-scrape-mismatch`](gcp-gke-cert-suite/cert-d9-02-gmp-podmonitoring-scrape-mismatch/task.yaml) | D9. Logging (FluentBit) & Managed Prometheus | `observability` | GCP PCDE | `gke-observability` |
| C42 | [`cert-d9-03-slo-error-budget-burn-rate-alert`](gcp-gke-cert-suite/cert-d9-03-slo-error-budget-burn-rate-alert/task.yaml) | D9. Logging (FluentBit) & Managed Prometheus | `observability` | GCP PCDE | `gke-alert-configuration` |
| C43 | [`cert-d9-04-cloud-logging-exclusion-filter`](gcp-gke-cert-suite/cert-d9-04-cloud-logging-exclusion-filter/task.yaml) | D9. Logging (FluentBit) & Managed Prometheus | `observability` | GCP PCDE / PCA | `gke-observability` |
| C44 | [`cert-d10-01-multi-cluster-services-export-import`](gcp-gke-cert-suite/cert-d10-01-multi-cluster-services-export-import/task.yaml) | D10. Fleet, Config Sync & Config Connector | `consistency` | GCP PCA / PCNE | `gke-service-networking` |
| C45 | [`cert-d10-02-configsync-mutation-ignore-hpa`](gcp-gke-cert-suite/cert-d10-02-configsync-mutation-ignore-hpa/task.yaml) | D10. Fleet, Config Sync & Config Connector | `consistency` | GCP PCDE | `gcp-config-connector` |

---

## Detailed Certification Scenarios

### C01: `cert-d1-01-autopilot-vs-standard-sizing` — GKE Autopilot vs Standard pod resource rounding and node management boundaries

- **1. Test Case ID & Title:** `cert-d1-01-autopilot-vs-standard-sizing` — _GKE Autopilot vs Standard pod resource rounding and node management boundaries_ ([task.yaml](gcp-gke-cert-suite/cert-d1-01-autopilot-vs-standard-sizing/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D1. Autoscaling, ComputeClass & Accelerators` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCA / ACE`
- **3. Target Skill:** `gke-compute-classes`
- **4. Scenario Prompt:** Our platform team is migrating a Deployment to a GKE Autopilot cluster and wants to run manual `kubectl drain` commands on nodes during maintenance while setting container CPU requests to `50m` on a general-purpose workload without a custom ComputeClass. Explain why both assumptions fail on GKE Autopilot, what Autopilot does to pod resource requests below the minimum floor, and how to target specific hardware families on Autopilot. Start your answer with `VERDICT: AUTOPILOT-MANAGES-NODES-AND-ENFORCES-POD-MINIMUMS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: AUTOPILOT-MANAGES-NODES-AND-ENFORCES-POD-MINIMUMS. On GKE Autopilot, Google manages node provisioning, draining, and patching (operators cannot manually `kubectl drain` nodes), and Autopilot enforces minimum pod CPU/memory floors (rounding up sub-minimum requests or rejecting invalid ratios). Workloads select hardware families using `cloud.google.com/compute-class` in `nodeSelector`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: AUTOPILOT-MANAGES-NODES-AND-ENFORCES-POD-MINIMUMS', 'cloud.google.com/compute-class', 'nodeSelector']`

```yaml
# Certification Exam Domain Probe (GCP PCA / ACE) — D1. Autoscaling, ComputeClass & Accelerators
# Target skill: gke-compute-classes
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d1-01-autopilot-vs-standard-sizing
name: "GKE Autopilot vs Standard pod resource rounding and node management boundaries"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  Our platform team is migrating a Deployment to a GKE Autopilot cluster and wants to run manual `kubectl drain` commands on nodes during maintenance while setting container CPU requests to `50m` on a general-purpose workload without a custom ComputeClass. Explain why both assumptions fail on GKE Autopilot, what Autopilot does to pod resource requests below the minimum floor, and how to target specific hardware families on Autopilot. Start your answer with `VERDICT: AUTOPILOT-MANAGES-NODES-AND-ENFORCES-POD-MINIMUMS`. Do not apply anything.
expected_output: >-
  VERDICT: AUTOPILOT-MANAGES-NODES-AND-ENFORCES-POD-MINIMUMS. On GKE Autopilot, Google manages node provisioning, draining, and patching (operators cannot manually `kubectl drain` nodes), and Autopilot enforces minimum pod CPU/memory floors (rounding up sub-minimum requests or rejecting invalid ratios). Workloads select hardware families using `cloud.google.com/compute-class` in `nodeSelector`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: AUTOPILOT-MANAGES-NODES-AND-ENFORCES-POD-MINIMUMS",
          "cloud.google.com/compute-class",
          "nodeSelector",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C02: `cert-d1-02-topology-spread-vs-antiaffinity` — Zonal pod skew prevention using topologySpreadConstraints with DoNotSchedule

- **1. Test Case ID & Title:** `cert-d1-02-topology-spread-vs-antiaffinity` — _Zonal pod skew prevention using topologySpreadConstraints with DoNotSchedule_ ([task.yaml](gcp-gke-cert-suite/cert-d1-02-topology-spread-vs-antiaffinity/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D1. Autoscaling, ComputeClass & Accelerators` | **`domains.yaml`:** `capacity` | **Exam Source:** `CNCF CKA / GCP PCA`
- **3. Target Skill:** `gke-workload-scaling`
- **4. Scenario Prompt:** Our 6-replica Deployment `checkout-api` (labelled `app: checkout-api`) on a 3-zone regional GKE cluster in `us-central1` piled 5 of its 6 replicas into `us-central1-a` because the manifest used `whenUnsatisfiable: ScheduleAnyway`. Give the exact `topologySpreadConstraints` YAML block to enforce a strict maximum zonal difference of 1 pod across zones and block scheduling if violated. Start your answer with `VERDICT: USE-DONOTSCHEDULE-MAXSKEW-1`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: USE-DONOTSCHEDULE-MAXSKEW-1. Configure `topologySpreadConstraints` with `maxSkew: 1`, `topologyKey: topology.kubernetes.io/zone`, `whenUnsatisfiable: DoNotSchedule`, and `labelSelector.matchLabels.app: checkout-api`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: USE-DONOTSCHEDULE-MAXSKEW-1', 'topology.kubernetes.io/zone', 'DoNotSchedule', 'maxSkew']`

```yaml
# Certification Exam Domain Probe (CNCF CKA / GCP PCA) — D1. Autoscaling, ComputeClass & Accelerators
# Target skill: gke-workload-scaling
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d1-02-topology-spread-vs-antiaffinity
name: "Zonal pod skew prevention using topologySpreadConstraints with DoNotSchedule"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  Our 6-replica Deployment `checkout-api` (labelled `app: checkout-api`) on a 3-zone regional GKE cluster in `us-central1` piled 5 of its 6 replicas into `us-central1-a` because the manifest used `whenUnsatisfiable: ScheduleAnyway`. Give the exact `topologySpreadConstraints` YAML block to enforce a strict maximum zonal difference of 1 pod across zones and block scheduling if violated. Start your answer with `VERDICT: USE-DONOTSCHEDULE-MAXSKEW-1`. Do not apply anything.
expected_output: >-
  VERDICT: USE-DONOTSCHEDULE-MAXSKEW-1. Configure `topologySpreadConstraints` with `maxSkew: 1`, `topologyKey: topology.kubernetes.io/zone`, `whenUnsatisfiable: DoNotSchedule`, and `labelSelector.matchLabels.app: checkout-api`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: USE-DONOTSCHEDULE-MAXSKEW-1",
          "topology.kubernetes.io/zone",
          "DoNotSchedule",
          "maxSkew",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C03: `cert-d1-03-priorityclass-preemption-pdb` — Non-preempting PriorityClass configuration to protect serving workloads

- **1. Test Case ID & Title:** `cert-d1-03-priorityclass-preemption-pdb` — _Non-preempting PriorityClass configuration to protect serving workloads_ ([task.yaml](gcp-gke-cert-suite/cert-d1-03-priorityclass-preemption-pdb/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D1. Autoscaling, ComputeClass & Accelerators` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCDE / CNCF CKA`
- **3. Target Skill:** `gke-workload-scaling`
- **4. Scenario Prompt:** High-priority batch jobs (`PriorityClass` value `100000`) are evicting latency-sensitive serving pods when our GKE node pool hits its autoscaler cap, even when we only want the batch jobs placed ahead of lower-priority pending pods in the scheduling queue without evicting running pods. Which `PriorityClass` field prevents live pod eviction while keeping queue priority? Start your answer with `VERDICT: SET-PREEMPTIONPOLICY-NEVER`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: SET-PREEMPTIONPOLICY-NEVER. Set `preemptionPolicy: Never` on the `PriorityClass` (instead of the default `PreemptLowerPriority`) so high-priority batch pods are prioritized in the scheduling queue ahead of lower-priority pending pods without preempting running pods.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: SET-PREEMPTIONPOLICY-NEVER', 'preemptionPolicy', 'Never', 'PriorityClass']`

```yaml
# Certification Exam Domain Probe (GCP PCDE / CNCF CKA) — D1. Autoscaling, ComputeClass & Accelerators
# Target skill: gke-workload-scaling
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d1-03-priorityclass-preemption-pdb
name: "Non-preempting PriorityClass configuration to protect serving workloads"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  High-priority batch jobs (`PriorityClass` value `100000`) are evicting latency-sensitive serving pods when our GKE node pool hits its autoscaler cap, even when we only want the batch jobs placed ahead of lower-priority pending pods in the scheduling queue without evicting running pods. Which `PriorityClass` field prevents live pod eviction while keeping queue priority? Start your answer with `VERDICT: SET-PREEMPTIONPOLICY-NEVER`. Do not apply anything.
expected_output: >-
  VERDICT: SET-PREEMPTIONPOLICY-NEVER. Set `preemptionPolicy: Never` on the `PriorityClass` (instead of the default `PreemptLowerPriority`) so high-priority batch pods are prioritized in the scheduling queue ahead of lower-priority pending pods without preempting running pods.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: SET-PREEMPTIONPOLICY-NEVER",
          "preemptionPolicy",
          "Never",
          "PriorityClass",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C04: `cert-d1-04-spot-vm-graceful-termination` — GKE Spot VM pod selector and graceful SIGTERM shutdown within preemption window

- **1. Test Case ID & Title:** `cert-d1-04-spot-vm-graceful-termination` — _GKE Spot VM pod selector and graceful SIGTERM shutdown within preemption window_ ([task.yaml](gcp-gke-cert-suite/cert-d1-04-spot-vm-graceful-termination/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D1. Autoscaling, ComputeClass & Accelerators` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCA / PCDE`
- **3. Target Skill:** `gke-compute-classes`
- **4. Scenario Prompt:** We want stateless worker pods to schedule onto GKE Spot VMs and gracefully flush in-flight work when Compute Engine sends a preemption notice. Give the exact `nodeSelector` label key/value for GKE Spot VMs and the pod spec fields required to handle graceful shutdown within the Spot preemption window. Start your answer with `VERDICT: GKE-SPOT-SELECTOR-AND-GRACE-PERIOD`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: GKE-SPOT-SELECTOR-AND-GRACE-PERIOD. Target Spot nodes with `cloud.google.com/gke-spot: "true"` in `nodeSelector` and configure `terminationGracePeriodSeconds` (up to 30 seconds on Spot preemption) alongside a container `preStop` hook or `SIGTERM` handler.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: GKE-SPOT-SELECTOR-AND-GRACE-PERIOD', 'cloud.google.com/gke-spot', 'terminationGracePeriodSeconds']`

```yaml
# Certification Exam Domain Probe (GCP PCA / PCDE) — D1. Autoscaling, ComputeClass & Accelerators
# Target skill: gke-compute-classes
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d1-04-spot-vm-graceful-termination
name: "GKE Spot VM pod selector and graceful SIGTERM shutdown within preemption window"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  We want stateless worker pods to schedule onto GKE Spot VMs and gracefully flush in-flight work when Compute Engine sends a preemption notice. Give the exact `nodeSelector` label key/value for GKE Spot VMs and the pod spec fields required to handle graceful shutdown within the Spot preemption window. Start your answer with `VERDICT: GKE-SPOT-SELECTOR-AND-GRACE-PERIOD`. Do not apply anything.
expected_output: >-
  VERDICT: GKE-SPOT-SELECTOR-AND-GRACE-PERIOD. Target Spot nodes with `cloud.google.com/gke-spot: "true"` in `nodeSelector` and configure `terminationGracePeriodSeconds` (up to 30 seconds on Spot preemption) alongside a container `preStop` hook or `SIGTERM` handler.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: GKE-SPOT-SELECTOR-AND-GRACE-PERIOD",
          "cloud.google.com/gke-spot",
          "terminationGracePeriodSeconds",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C05: `cert-d1-05-gpu-time-sharing-vs-mig` — Multi-Instance GPU (MIG) vs time-sharing for hardware fault and memory isolation

- **1. Test Case ID & Title:** `cert-d1-05-gpu-time-sharing-vs-mig` — _Multi-Instance GPU (MIG) vs time-sharing for hardware fault and memory isolation_ ([task.yaml](gcp-gke-cert-suite/cert-d1-05-gpu-time-sharing-vs-mig/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D1. Autoscaling, ComputeClass & Accelerators` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCA / PCDE`
- **3. Target Skill:** `gke-batch-hpc`
- **4. Scenario Prompt:** Two multi-tenant inference teams share NVIDIA A100 GPUs on GKE and require strict hardware memory and fault isolation so an OOM or CUDA fault in Team A's container cannot affect Team B. Should we configure GPU time-sharing (`maxSharedClientsPerGpu`) or Multi-Instance GPU (MIG) partitions (such as `nvidia.com/mig-1g.5gb`)? Start your answer with `VERDICT: USE-MULTI-INSTANCE-GPU-MIG`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: USE-MULTI-INSTANCE-GPU-MIG. Multi-Instance GPU (MIG, e.g. `nvidia.com/mig-1g.5gb`) partitions an A100/H100 GPU into separate hardware instances with dedicated high-bandwidth memory and compute engines, providing hardware fault and memory isolation that software time-sharing (`maxSharedClientsPerGpu`) does not provide.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: USE-MULTI-INSTANCE-GPU-MIG', 'nvidia.com/mig', 'maxSharedClientsPerGpu']`

```yaml
# Certification Exam Domain Probe (GCP PCA / PCDE) — D1. Autoscaling, ComputeClass & Accelerators
# Target skill: gke-batch-hpc
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d1-05-gpu-time-sharing-vs-mig
name: "Multi-Instance GPU (MIG) vs time-sharing for hardware fault and memory isolation"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  Two multi-tenant inference teams share NVIDIA A100 GPUs on GKE and require strict hardware memory and fault isolation so an OOM or CUDA fault in Team A's container cannot affect Team B. Should we configure GPU time-sharing (`maxSharedClientsPerGpu`) or Multi-Instance GPU (MIG) partitions (such as `nvidia.com/mig-1g.5gb`)? Start your answer with `VERDICT: USE-MULTI-INSTANCE-GPU-MIG`. Do not apply anything.
expected_output: >-
  VERDICT: USE-MULTI-INSTANCE-GPU-MIG. Multi-Instance GPU (MIG, e.g. `nvidia.com/mig-1g.5gb`) partitions an A100/H100 GPU into separate hardware instances with dedicated high-bandwidth memory and compute engines, providing hardware fault and memory isolation that software time-sharing (`maxSharedClientsPerGpu`) does not provide.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: USE-MULTI-INSTANCE-GPU-MIG",
          "nvidia.com/mig",
          "maxSharedClientsPerGpu",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C06: `cert-d2-01-release-channel-selection` — GKE Release Channel selection and maintenance exclusion window flags

- **1. Test Case ID & Title:** `cert-d2-01-release-channel-selection` — _GKE Release Channel selection and maintenance exclusion window flags_ ([task.yaml](gcp-gke-cert-suite/cert-d2-01-release-channel-selection/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D2. Cluster & Node Upgrades & APIs` | **`domains.yaml`:** `upgrades` | **Exam Source:** `GCP PCA / ACE`
- **3. Target Skill:** `gke-upgrades`
- **4. Scenario Prompt:** A regulated payments cluster needs conservative, battle-tested Kubernetes versions while temporarily blocking automatic node and control-plane minor upgrades during a 14-day peak retail freeze. Which GKE `--release-channel` value should it use (`rapid`, `regular`, or `stable`), and which `gcloud container clusters update` flags register a maintenance exclusion with scope `no_minor_or_node_upgrades`? Start your answer with `VERDICT: STABLE-CHANNEL-WITH-MAINTENANCE-EXCLUSION`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: STABLE-CHANNEL-WITH-MAINTENANCE-EXCLUSION. Use `--release-channel=stable` and register an exclusion with `gcloud container clusters update <cluster> --add-maintenance-exclusion-name=<name> --add-maintenance-exclusion-start=<timestamp> --add-maintenance-exclusion-end=<timestamp> --add-maintenance-exclusion-scope=no_minor_or_node_upgrades`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: STABLE-CHANNEL-WITH-MAINTENANCE-EXCLUSION', '--add-maintenance-exclusion-end', 'no_minor_or_node_upgrades']`

```yaml
# Certification Exam Domain Probe (GCP PCA / ACE) — D2. Cluster & Node Upgrades & APIs
# Target skill: gke-upgrades
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d2-01-release-channel-selection
name: "GKE Release Channel selection and maintenance exclusion window flags"
domain: upgrades
owner: toshiowang
expected_fail: true

prompt: >-
  A regulated payments cluster needs conservative, battle-tested Kubernetes versions while temporarily blocking automatic node and control-plane minor upgrades during a 14-day peak retail freeze. Which GKE `--release-channel` value should it use (`rapid`, `regular`, or `stable`), and which `gcloud container clusters update` flags register a maintenance exclusion with scope `no_minor_or_node_upgrades`? Start your answer with `VERDICT: STABLE-CHANNEL-WITH-MAINTENANCE-EXCLUSION`. Do not apply anything.
expected_output: >-
  VERDICT: STABLE-CHANNEL-WITH-MAINTENANCE-EXCLUSION. Use `--release-channel=stable` and register an exclusion with `gcloud container clusters update <cluster> --add-maintenance-exclusion-name=<name> --add-maintenance-exclusion-start=<timestamp> --add-maintenance-exclusion-end=<timestamp> --add-maintenance-exclusion-scope=no_minor_or_node_upgrades`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: STABLE-CHANNEL-WITH-MAINTENANCE-EXCLUSION",
          "--add-maintenance-exclusion-end",
          "no_minor_or_node_upgrades",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C07: `cert-d2-02-blue-green-nodepool-soak-rollback` — Blue-green node pool upgrade soak duration and rollback mechanics

- **1. Test Case ID & Title:** `cert-d2-02-blue-green-nodepool-soak-rollback` — _Blue-green node pool upgrade soak duration and rollback mechanics_ ([task.yaml](gcp-gke-cert-suite/cert-d2-02-blue-green-nodepool-soak-rollback/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D2. Cluster & Node Upgrades & APIs` | **`domains.yaml`:** `upgrades` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-upgrades`
- **4. Scenario Prompt:** Our stateful Cassandra node pool on GKE Standard needs an upgrade strategy that provisions a full replacement green pool, cordons and drains the blue pool, keeps the blue nodes around for a 24-hour soak window so we can roll back immediately if latency spikes, and exposes a single `gcloud` rollback command during that window. Give the exact `gcloud container node-pools update` flags to enable this and the rollback subcommand. Start your answer with `VERDICT: ENABLE-BLUE-GREEN-UPGRADE-WITH-SOAK`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ENABLE-BLUE-GREEN-UPGRADE-WITH-SOAK. Configure blue-green upgrades with `gcloud container node-pools update <pool> --enable-blue-green-upgrade --node-pool-soak-duration=86400s` and roll back during the soak phase using `gcloud container node-pools rollback <pool>`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ENABLE-BLUE-GREEN-UPGRADE-WITH-SOAK', '--enable-blue-green-upgrade', '--node-pool-soak-duration', 'node-pools rollback']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D2. Cluster & Node Upgrades & APIs
# Target skill: gke-upgrades
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d2-02-blue-green-nodepool-soak-rollback
name: "Blue-green node pool upgrade soak duration and rollback mechanics"
domain: upgrades
owner: toshiowang
expected_fail: true

prompt: >-
  Our stateful Cassandra node pool on GKE Standard needs an upgrade strategy that provisions a full replacement green pool, cordons and drains the blue pool, keeps the blue nodes around for a 24-hour soak window so we can roll back immediately if latency spikes, and exposes a single `gcloud` rollback command during that window. Give the exact `gcloud container node-pools update` flags to enable this and the rollback subcommand. Start your answer with `VERDICT: ENABLE-BLUE-GREEN-UPGRADE-WITH-SOAK`. Do not apply anything.
expected_output: >-
  VERDICT: ENABLE-BLUE-GREEN-UPGRADE-WITH-SOAK. Configure blue-green upgrades with `gcloud container node-pools update <pool> --enable-blue-green-upgrade --node-pool-soak-duration=86400s` and roll back during the soak phase using `gcloud container node-pools rollback <pool>`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ENABLE-BLUE-GREEN-UPGRADE-WITH-SOAK",
          "--enable-blue-green-upgrade",
          "--node-pool-soak-duration",
          "node-pools rollback",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C08: `cert-d3-01-vpa-hpa-cpu-conflict` — Resolving VPA Auto mode and HPA CPU co-management replica thrashing

- **1. Test Case ID & Title:** `cert-d3-01-vpa-hpa-cpu-conflict` — _Resolving VPA Auto mode and HPA CPU co-management replica thrashing_ ([task.yaml](gcp-gke-cert-suite/cert-d3-01-vpa-hpa-cpu-conflict/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D3. Workloads, OOM, Probes & HPA` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-workload-scaling`
- **4. Scenario Prompt:** A Deployment on GKE has both a `HorizontalPodAutoscaler` scaling on average CPU utilization and a `VerticalPodAutoscaler` with `updateMode: Auto` adjusting CPU requests, causing continuous pod restarts and replica count oscillation. Explain why VPA and HPA conflict on CPU/memory and how to configure `updateMode` or HPA metric types according to GKE best practices. Start your answer with `VERDICT: DO-NOT-COMANAGE-CPU-WITH-VPA-AUTO-AND-HPA`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: DO-NOT-COMANAGE-CPU-WITH-VPA-AUTO-AND-HPA. VPA `updateMode: Auto` mutates pod CPU requests and evicts pods while HPA calculates replica counts from CPU utilization against those same requests. Fix by setting VPA `updateMode: Off` (recommendation-only) when HPA scales on CPU/memory, or use HPA with custom/external request-rate metrics only.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: DO-NOT-COMANAGE-CPU-WITH-VPA-AUTO-AND-HPA', 'updateMode', 'HorizontalPodAutoscaler', 'VerticalPodAutoscaler']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D3. Workloads, OOM, Probes & HPA
# Target skill: gke-workload-scaling
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d3-01-vpa-hpa-cpu-conflict
name: "Resolving VPA Auto mode and HPA CPU co-management replica thrashing"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  A Deployment on GKE has both a `HorizontalPodAutoscaler` scaling on average CPU utilization and a `VerticalPodAutoscaler` with `updateMode: Auto` adjusting CPU requests, causing continuous pod restarts and replica count oscillation. Explain why VPA and HPA conflict on CPU/memory and how to configure `updateMode` or HPA metric types according to GKE best practices. Start your answer with `VERDICT: DO-NOT-COMANAGE-CPU-WITH-VPA-AUTO-AND-HPA`. Do not apply anything.
expected_output: >-
  VERDICT: DO-NOT-COMANAGE-CPU-WITH-VPA-AUTO-AND-HPA. VPA `updateMode: Auto` mutates pod CPU requests and evicts pods while HPA calculates replica counts from CPU utilization against those same requests. Fix by setting VPA `updateMode: Off` (recommendation-only) when HPA scales on CPU/memory, or use HPA with custom/external request-rate metrics only.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: DO-NOT-COMANAGE-CPU-WITH-VPA-AUTO-AND-HPA",
          "updateMode",
          "HorizontalPodAutoscaler",
          "VerticalPodAutoscaler",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C09: `cert-d3-02-startup-vs-liveness-probe-deadlock` — Preventing livenessProbe restart loops on slow-starting containers with startupProbe

- **1. Test Case ID & Title:** `cert-d3-02-startup-vs-liveness-probe-deadlock` — _Preventing livenessProbe restart loops on slow-starting containers with startupProbe_ ([task.yaml](gcp-gke-cert-suite/cert-d3-02-startup-vs-liveness-probe-deadlock/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D3. Workloads, OOM, Probes & HPA` | **`domains.yaml`:** `reliability` | **Exam Source:** `CNCF CKAD / GCP PCDE`
- **3. Target Skill:** `gke-reliability`
- **4. Scenario Prompt:** A legacy Java service on GKE takes up to 120 seconds to warm caches on cold start, but once started it must be restarted within 15 seconds if its `/healthz` endpoint deadlocks. Right now `livenessProbe` (`periodSeconds: 5, failureThreshold: 3`) kills the container every 15 seconds before startup finishes. Give the exact Kubernetes probe configuration that allows up to 120s for startup while keeping fast 15s deadlock detection afterward. Start your answer with `VERDICT: ADD-STARTUPPROBE-GUARDING-LIVENESSPROBE`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ADD-STARTUPPROBE-GUARDING-LIVENESSPROBE. Add a `startupProbe` on `/healthz` with `periodSeconds: 5` and `failureThreshold: 24` (5s * 24 = 120s startup budget); Kubernetes disables `livenessProbe` until `startupProbe` succeeds once, preserving the 15s (`periodSeconds: 5, failureThreshold: 3`) `livenessProbe` afterward.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ADD-STARTUPPROBE-GUARDING-LIVENESSPROBE', 'startupProbe', 'livenessProbe', 'failureThreshold']`

```yaml
# Certification Exam Domain Probe (CNCF CKAD / GCP PCDE) — D3. Workloads, OOM, Probes & HPA
# Target skill: gke-reliability
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d3-02-startup-vs-liveness-probe-deadlock
name: "Preventing livenessProbe restart loops on slow-starting containers with startupProbe"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  A legacy Java service on GKE takes up to 120 seconds to warm caches on cold start, but once started it must be restarted within 15 seconds if its `/healthz` endpoint deadlocks. Right now `livenessProbe` (`periodSeconds: 5, failureThreshold: 3`) kills the container every 15 seconds before startup finishes. Give the exact Kubernetes probe configuration that allows up to 120s for startup while keeping fast 15s deadlock detection afterward. Start your answer with `VERDICT: ADD-STARTUPPROBE-GUARDING-LIVENESSPROBE`. Do not apply anything.
expected_output: >-
  VERDICT: ADD-STARTUPPROBE-GUARDING-LIVENESSPROBE. Add a `startupProbe` on `/healthz` with `periodSeconds: 5` and `failureThreshold: 24` (5s * 24 = 120s startup budget); Kubernetes disables `livenessProbe` until `startupProbe` succeeds once, preserving the 15s (`periodSeconds: 5, failureThreshold: 3`) `livenessProbe` afterward.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ADD-STARTUPPROBE-GUARDING-LIVENESSPROBE",
          "startupProbe",
          "livenessProbe",
          "failureThreshold",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C10: `cert-d3-03-initcontainer-ordering-and-sidecar` — Native Kubernetes sidecar containers using initContainers with restartPolicy Always

- **1. Test Case ID & Title:** `cert-d3-03-initcontainer-ordering-and-sidecar` — _Native Kubernetes sidecar containers using initContainers with restartPolicy Always_ ([task.yaml](gcp-gke-cert-suite/cert-d3-03-initcontainer-ordering-and-sidecar/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D3. Workloads, OOM, Probes & HPA` | **`domains.yaml`:** `reliability` | **Exam Source:** `CNCF CKA / CKAD`
- **3. Target Skill:** `gke-reliability`
- **4. Scenario Prompt:** A Kubernetes `Job` on GKE 1.29+ runs a batch worker alongside a Cloud SQL Auth Proxy container in `spec.containers`. When the batch worker finishes with exit code 0, the Pod never completes because the proxy container keeps running. How do you configure the proxy as a native Kubernetes sidecar so it starts before the main worker and automatically terminates when the Job container exits? Start your answer with `VERDICT: INITCONTAINER-WITH-RESTARTPOLICY-ALWAYS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: INITCONTAINER-WITH-RESTARTPOLICY-ALWAYS. Define the proxy under `spec.initContainers` with `restartPolicy: Always`. Kubernetes starts the native sidecar before the main Job container and terminates it automatically once all regular containers in `spec.containers` exit.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: INITCONTAINER-WITH-RESTARTPOLICY-ALWAYS', 'initContainers', 'restartPolicy: Always']`

```yaml
# Certification Exam Domain Probe (CNCF CKA / CKAD) — D3. Workloads, OOM, Probes & HPA
# Target skill: gke-reliability
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d3-03-initcontainer-ordering-and-sidecar
name: "Native Kubernetes sidecar containers using initContainers with restartPolicy Always"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  A Kubernetes `Job` on GKE 1.29+ runs a batch worker alongside a Cloud SQL Auth Proxy container in `spec.containers`. When the batch worker finishes with exit code 0, the Pod never completes because the proxy container keeps running. How do you configure the proxy as a native Kubernetes sidecar so it starts before the main worker and automatically terminates when the Job container exits? Start your answer with `VERDICT: INITCONTAINER-WITH-RESTARTPOLICY-ALWAYS`. Do not apply anything.
expected_output: >-
  VERDICT: INITCONTAINER-WITH-RESTARTPOLICY-ALWAYS. Define the proxy under `spec.initContainers` with `restartPolicy: Always`. Kubernetes starts the native sidecar before the main Job container and terminates it automatically once all regular containers in `spec.containers` exit.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: INITCONTAINER-WITH-RESTARTPOLICY-ALWAYS",
          "initContainers",
          "restartPolicy: Always",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C11: `cert-d3-04-native-service-canary-split` — Native Kubernetes canary traffic splitting across two Deployments behind one Service

- **1. Test Case ID & Title:** `cert-d3-04-native-service-canary-split` — _Native Kubernetes canary traffic splitting across two Deployments behind one Service_ ([task.yaml](gcp-gke-cert-suite/cert-d3-04-native-service-canary-split/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D3. Workloads, OOM, Probes & HPA` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-service-networking`
- **4. Scenario Prompt:** Without installing a service mesh or spinning up a second GKE cluster, how do you route approximately 10% of intra-cluster traffic to `v2` of a microservice (`orders-canary`) and 90% to `v1` (`orders-stable`) using only native Kubernetes `Deployment` and `Service` objects? Start your answer with `VERDICT: SHARED-SERVICE-SELECTOR-ACROSS-TWO-DEPLOYMENTS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: SHARED-SERVICE-SELECTOR-ACROSS-TWO-DEPLOYMENTS. Run two Deployments (`orders-stable` with 9 replicas and `orders-canary` with 1 replica) whose Pod templates share a common label (for example `app: orders`) matched by the single Kubernetes `Service` `spec.selector`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: SHARED-SERVICE-SELECTOR-ACROSS-TWO-DEPLOYMENTS', 'orders-stable', 'orders-canary', 'selector']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D3. Workloads, OOM, Probes & HPA
# Target skill: gke-service-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d3-04-native-service-canary-split
name: "Native Kubernetes canary traffic splitting across two Deployments behind one Service"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  Without installing a service mesh or spinning up a second GKE cluster, how do you route approximately 10% of intra-cluster traffic to `v2` of a microservice (`orders-canary`) and 90% to `v1` (`orders-stable`) using only native Kubernetes `Deployment` and `Service` objects? Start your answer with `VERDICT: SHARED-SERVICE-SELECTOR-ACROSS-TWO-DEPLOYMENTS`. Do not apply anything.
expected_output: >-
  VERDICT: SHARED-SERVICE-SELECTOR-ACROSS-TWO-DEPLOYMENTS. Run two Deployments (`orders-stable` with 9 replicas and `orders-canary` with 1 replica) whose Pod templates share a common label (for example `app: orders`) matched by the single Kubernetes `Service` `spec.selector`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: SHARED-SERVICE-SELECTOR-ACROSS-TWO-DEPLOYMENTS",
          "orders-stable",
          "orders-canary",
          "selector",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C12: `cert-d3-05-resourcequota-limitrange-admission` — Resolving ResourceQuota admission rejections with a namespace LimitRange

- **1. Test Case ID & Title:** `cert-d3-05-resourcequota-limitrange-admission` — _Resolving ResourceQuota admission rejections with a namespace LimitRange_ ([task.yaml](gcp-gke-cert-suite/cert-d3-05-resourcequota-limitrange-admission/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D3. Workloads, OOM, Probes & HPA` | **`domains.yaml`:** `reliability` | **Exam Source:** `CNCF CKA / GCP PCA`
- **3. Target Skill:** `gke-multitenancy`
- **4. Scenario Prompt:** After a platform admin applied a `ResourceQuota` enforcing `requests.cpu`, `limits.cpu`, `requests.memory`, and `limits.memory` in namespace `team-alpha`, developers' Deployments that omit explicit container `resources` blocks fail admission with `Error creating: pods is forbidden: failed quota: must specify limits.cpu,limits.memory`. Which Kubernetes object should the admin add to `team-alpha` so pods omitting resource blocks receive automatic defaults? Start your answer with `VERDICT: DEPLOY-NAMESPACE-LIMITRANGE-DEFAULTS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: DEPLOY-NAMESPACE-LIMITRANGE-DEFAULTS. Create a `LimitRange` in namespace `team-alpha` with `type: Container`, `default` (default limits), and `defaultRequest` (default requests) so the LimitRanger admission controller injects defaults before `ResourceQuota` validation.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: DEPLOY-NAMESPACE-LIMITRANGE-DEFAULTS', 'LimitRange', 'defaultRequest', 'ResourceQuota']`

```yaml
# Certification Exam Domain Probe (CNCF CKA / GCP PCA) — D3. Workloads, OOM, Probes & HPA
# Target skill: gke-multitenancy
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d3-05-resourcequota-limitrange-admission
name: "Resolving ResourceQuota admission rejections with a namespace LimitRange"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  After a platform admin applied a `ResourceQuota` enforcing `requests.cpu`, `limits.cpu`, `requests.memory`, and `limits.memory` in namespace `team-alpha`, developers' Deployments that omit explicit container `resources` blocks fail admission with `Error creating: pods is forbidden: failed quota: must specify limits.cpu,limits.memory`. Which Kubernetes object should the admin add to `team-alpha` so pods omitting resource blocks receive automatic defaults? Start your answer with `VERDICT: DEPLOY-NAMESPACE-LIMITRANGE-DEFAULTS`. Do not apply anything.
expected_output: >-
  VERDICT: DEPLOY-NAMESPACE-LIMITRANGE-DEFAULTS. Create a `LimitRange` in namespace `team-alpha` with `type: Container`, `default` (default limits), and `defaultRequest` (default requests) so the LimitRanger admission controller injects defaults before `ResourceQuota` validation.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: DEPLOY-NAMESPACE-LIMITRANGE-DEFAULTS",
          "LimitRange",
          "defaultRequest",
          "ResourceQuota",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C13: `cert-d3-06-jobset-gang-scheduling-recovery` — JobSet coordinated startup order and failure recovery for distributed AI workloads

- **1. Test Case ID & Title:** `cert-d3-06-jobset-gang-scheduling-recovery` — _JobSet coordinated startup order and failure recovery for distributed AI workloads_ ([task.yaml](gcp-gke-cert-suite/cert-d3-06-jobset-gang-scheduling-recovery/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D3. Workloads, OOM, Probes & HPA` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-ai-troubleshooting-jobset-interruption`
- **4. Scenario Prompt:** Our distributed training `JobSet` on GKE has a `leader` `replicatedJob` and a `workers` `replicatedJob`. Right now workers start before the leader is ready, and when a node preempts one worker pod with exit code `137`, the JobSet restarts beyond our max retry budget. Which `JobSet` spec fields enforce in-order replicatedJob startup and controlled failure restarts? Start your answer with `VERDICT: CONFIGURE-STARTUPPOLICY-INORDER-AND-FAILUREPOLICY`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: CONFIGURE-STARTUPPOLICY-INORDER-AND-FAILUREPOLICY. Configure `startupPolicy.startupPolicyOrder: InOrder` on the `JobSet` spec so the first `replicatedJob` (`leader`) reaches ready before `workers` start, and define `failurePolicy.maxRestarts` and `failurePolicy.rules` (`RecreateJobSet`).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: CONFIGURE-STARTUPPOLICY-INORDER-AND-FAILUREPOLICY', 'startupPolicy', 'InOrder', 'failurePolicy']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D3. Workloads, OOM, Probes & HPA
# Target skill: gke-ai-troubleshooting-jobset-interruption
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d3-06-jobset-gang-scheduling-recovery
name: "JobSet coordinated startup order and failure recovery for distributed AI workloads"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  Our distributed training `JobSet` on GKE has a `leader` `replicatedJob` and a `workers` `replicatedJob`. Right now workers start before the leader is ready, and when a node preempts one worker pod with exit code `137`, the JobSet restarts beyond our max retry budget. Which `JobSet` spec fields enforce in-order replicatedJob startup and controlled failure restarts? Start your answer with `VERDICT: CONFIGURE-STARTUPPOLICY-INORDER-AND-FAILUREPOLICY`. Do not apply anything.
expected_output: >-
  VERDICT: CONFIGURE-STARTUPPOLICY-INORDER-AND-FAILUREPOLICY. Configure `startupPolicy.startupPolicyOrder: InOrder` on the `JobSet` spec so the first `replicatedJob` (`leader`) reaches ready before `workers` start, and define `failurePolicy.maxRestarts` and `failurePolicy.rules` (`RecreateJobSet`).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: CONFIGURE-STARTUPPOLICY-INORDER-AND-FAILUREPOLICY",
          "startupPolicy",
          "InOrder",
          "failurePolicy",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C14: `cert-d4-01-gke-cost-allocation-bigquery` — Enabling GKE Cost Allocation for namespace and label chargeback in BigQuery

- **1. Test Case ID & Title:** `cert-d4-01-gke-cost-allocation-bigquery` — _Enabling GKE Cost Allocation for namespace and label chargeback in BigQuery_ ([task.yaml](gcp-gke-cert-suite/cert-d4-01-gke-cost-allocation-bigquery/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D4. Control Plane, Setup, Cost & CLI` | **`domains.yaml`:** `cost` | **Exam Source:** `GCP PCA / PCDE`
- **3. Target Skill:** `gke-cost-analysis`
- **4. Scenario Prompt:** Finance wants to break down GKE cluster spend by Kubernetes namespace and pod `env` / `team` labels inside our Cloud Billing detailed usage cost export in BigQuery. Give the exact `gcloud container clusters update` flag to enable this feature on an existing cluster. Start your answer with `VERDICT: ENABLE-GKE-COST-ALLOCATION`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ENABLE-GKE-COST-ALLOCATION. Run `gcloud container clusters update <cluster> --location=<location> --enable-cost-allocation` so GKE exports namespace and Kubernetes label (`k8s-namespace`, `kube_labels`) resource consumption to the Cloud Billing BigQuery table.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ENABLE-GKE-COST-ALLOCATION', '--enable-cost-allocation', 'BigQuery']`

```yaml
# Certification Exam Domain Probe (GCP PCA / PCDE) — D4. Control Plane, Setup, Cost & CLI
# Target skill: gke-cost-analysis
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d4-01-gke-cost-allocation-bigquery
name: "Enabling GKE Cost Allocation for namespace and label chargeback in BigQuery"
domain: cost
owner: toshiowang
expected_fail: true

prompt: >-
  Finance wants to break down GKE cluster spend by Kubernetes namespace and pod `env` / `team` labels inside our Cloud Billing detailed usage cost export in BigQuery. Give the exact `gcloud container clusters update` flag to enable this feature on an existing cluster. Start your answer with `VERDICT: ENABLE-GKE-COST-ALLOCATION`. Do not apply anything.
expected_output: >-
  VERDICT: ENABLE-GKE-COST-ALLOCATION. Run `gcloud container clusters update <cluster> --location=<location> --enable-cost-allocation` so GKE exports namespace and Kubernetes label (`k8s-namespace`, `kube_labels`) resource consumption to the Cloud Billing BigQuery table.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ENABLE-GKE-COST-ALLOCATION",
          "--enable-cost-allocation",
          "BigQuery",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C15: `cert-d4-02-private-cluster-vpn-custom-routes` — Reaching a private GKE control plane from on-premises over Cloud VPN and BGP custom routes

- **1. Test Case ID & Title:** `cert-d4-02-private-cluster-vpn-custom-routes` — _Reaching a private GKE control plane from on-premises over Cloud VPN and BGP custom routes_ ([task.yaml](gcp-gke-cert-suite/cert-d4-02-private-cluster-vpn-custom-routes/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D4. Control Plane, Setup, Cost & CLI` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCNE / PCA`
- **3. Target Skill:** `gke-networking`
- **4. Scenario Prompt:** An on-premises CI runner in `192.0.2.0/24` connects to our GCP VPC in `us-east1` through a Cloud VPN tunnel in `us-west1`, but `kubectl` times out reaching the private endpoint of our private GKE cluster in `us-east1` (master CIDR `198.51.100.0/28`). Which two settings (one on the GKE cluster and one on the Cloud Router BGP session) are required in addition to `masterAuthorizedNetworks`? Start your answer with `VERDICT: ENABLE-MASTER-GLOBAL-ACCESS-AND-CUSTOM-ROUTE-ADVERTISEMENT`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ENABLE-MASTER-GLOBAL-ACCESS-AND-CUSTOM-ROUTE-ADVERTISEMENT. Enable master global access on the cluster (`--enable-master-global-access`) so the private control plane is reachable across regions, and advertise the GKE control-plane `/28` range (`198.51.100.0/28`) as a custom advertised route on the Cloud Router BGP session (`--advertisement-mode=CUSTOM`).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ENABLE-MASTER-GLOBAL-ACCESS-AND-CUSTOM-ROUTE-ADVERTISEMENT', '--enable-master-global-access', 'Cloud Router']`

```yaml
# Certification Exam Domain Probe (GCP PCNE / PCA) — D4. Control Plane, Setup, Cost & CLI
# Target skill: gke-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d4-02-private-cluster-vpn-custom-routes
name: "Reaching a private GKE control plane from on-premises over Cloud VPN and BGP custom routes"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  An on-premises CI runner in `192.0.2.0/24` connects to our GCP VPC in `us-east1` through a Cloud VPN tunnel in `us-west1`, but `kubectl` times out reaching the private endpoint of our private GKE cluster in `us-east1` (master CIDR `198.51.100.0/28`). Which two settings (one on the GKE cluster and one on the Cloud Router BGP session) are required in addition to `masterAuthorizedNetworks`? Start your answer with `VERDICT: ENABLE-MASTER-GLOBAL-ACCESS-AND-CUSTOM-ROUTE-ADVERTISEMENT`. Do not apply anything.
expected_output: >-
  VERDICT: ENABLE-MASTER-GLOBAL-ACCESS-AND-CUSTOM-ROUTE-ADVERTISEMENT. Enable master global access on the cluster (`--enable-master-global-access`) so the private control plane is reachable across regions, and advertise the GKE control-plane `/28` range (`198.51.100.0/28`) as a custom advertised route on the Cloud Router BGP session (`--advertisement-mode=CUSTOM`).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ENABLE-MASTER-GLOBAL-ACCESS-AND-CUSTOM-ROUTE-ADVERTISEMENT",
          "--enable-master-global-access",
          "Cloud Router",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C16: `cert-d4-03-dns-endpoint-control-plane-auth` — Control-plane access via GKE DNS endpoint without IP authorized networks

- **1. Test Case ID & Title:** `cert-d4-03-dns-endpoint-control-plane-auth` — _Control-plane access via GKE DNS endpoint without IP authorized networks_ ([task.yaml](gcp-gke-cert-suite/cert-d4-03-dns-endpoint-control-plane-auth/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D4. Control Plane, Setup, Cost & CLI` | **`domains.yaml`:** `chat-and-routing` | **Exam Source:** `GCP ACE / PCA`
- **3. Target Skill:** `gke-basics`
- **4. Scenario Prompt:** Remote engineers without a static corporate egress IP need to run `kubectl` against our GKE cluster using IAM-authenticated control-plane DNS access rather than managing IP CIDRs in `masterAuthorizedNetworks`. Give the exact `gcloud container clusters update` flag to enable the DNS endpoint and the `gcloud container clusters get-credentials` flag engineers must pass. Start your answer with `VERDICT: ENABLE-DNS-ACCESS-AND-GET-CREDENTIALS-DNS-ENDPOINT`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ENABLE-DNS-ACCESS-AND-GET-CREDENTIALS-DNS-ENDPOINT. Enable DNS control-plane access with `gcloud container clusters update <cluster> --enable-dns-access` and generate the kubeconfig entry with `gcloud container clusters get-credentials <cluster> --dns-endpoint`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ENABLE-DNS-ACCESS-AND-GET-CREDENTIALS-DNS-ENDPOINT', '--enable-dns-access', '--dns-endpoint']`

```yaml
# Certification Exam Domain Probe (GCP ACE / PCA) — D4. Control Plane, Setup, Cost & CLI
# Target skill: gke-basics
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d4-03-dns-endpoint-control-plane-auth
name: "Control-plane access via GKE DNS endpoint without IP authorized networks"
domain: chat-and-routing
owner: toshiowang
expected_fail: true

prompt: >-
  Remote engineers without a static corporate egress IP need to run `kubectl` against our GKE cluster using IAM-authenticated control-plane DNS access rather than managing IP CIDRs in `masterAuthorizedNetworks`. Give the exact `gcloud container clusters update` flag to enable the DNS endpoint and the `gcloud container clusters get-credentials` flag engineers must pass. Start your answer with `VERDICT: ENABLE-DNS-ACCESS-AND-GET-CREDENTIALS-DNS-ENDPOINT`. Do not apply anything.
expected_output: >-
  VERDICT: ENABLE-DNS-ACCESS-AND-GET-CREDENTIALS-DNS-ENDPOINT. Enable DNS control-plane access with `gcloud container clusters update <cluster> --enable-dns-access` and generate the kubeconfig entry with `gcloud container clusters get-credentials <cluster> --dns-endpoint`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ENABLE-DNS-ACCESS-AND-GET-CREDENTIALS-DNS-ENDPOINT",
          "--enable-dns-access",
          "--dns-endpoint",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C17: `cert-d4-04-cluster-autoscaler-scale-down-blockers` — Diagnosing and remediating Cluster Autoscaler node scale-down blockers

- **1. Test Case ID & Title:** `cert-d4-04-cluster-autoscaler-scale-down-blockers` — _Diagnosing and remediating Cluster Autoscaler node scale-down blockers_ ([task.yaml](gcp-gke-cert-suite/cert-d4-04-cluster-autoscaler-scale-down-blockers/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D4. Control Plane, Setup, Cost & CLI` | **`domains.yaml`:** `cost` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-cluster-autoscaler`
- **4. Scenario Prompt:** Ten nodes in our GKE node pool sit at 8% CPU utilization for hours, but Cluster Autoscaler reports `no.scale.down.node.pod.not.backed.by.controller` and `no.scale.down.node.pod.kube.system.unmovable`. Name the three most common pod-level configurations that block Cluster Autoscaler from draining a node and how to allow safe eviction of pods using `emptyDir` scratch volumes. Start your answer with `VERDICT: SAFE-TO-EVICT-TRUE-AND-PDB-FOR-SYSTEM-PODS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: SAFE-TO-EVICT-TRUE-AND-PDB-FOR-SYSTEM-PODS. Scale-down is blocked by standalone pods not managed by a controller, `kube-system` pods lacking a `PodDisruptionBudget` (or restricted by `maxUnavailable: 0`), pods with `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"`, and pods with local `emptyDir` storage unless annotated with `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: SAFE-TO-EVICT-TRUE-AND-PDB-FOR-SYSTEM-PODS', 'cluster-autoscaler.kubernetes.io/safe-to-evict', 'PodDisruptionBudget', 'emptyDir']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D4. Control Plane, Setup, Cost & CLI
# Target skill: gke-cluster-autoscaler
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d4-04-cluster-autoscaler-scale-down-blockers
name: "Diagnosing and remediating Cluster Autoscaler node scale-down blockers"
domain: cost
owner: toshiowang
expected_fail: true

prompt: >-
  Ten nodes in our GKE node pool sit at 8% CPU utilization for hours, but Cluster Autoscaler reports `no.scale.down.node.pod.not.backed.by.controller` and `no.scale.down.node.pod.kube.system.unmovable`. Name the three most common pod-level configurations that block Cluster Autoscaler from draining a node and how to allow safe eviction of pods using `emptyDir` scratch volumes. Start your answer with `VERDICT: SAFE-TO-EVICT-TRUE-AND-PDB-FOR-SYSTEM-PODS`. Do not apply anything.
expected_output: >-
  VERDICT: SAFE-TO-EVICT-TRUE-AND-PDB-FOR-SYSTEM-PODS. Scale-down is blocked by standalone pods not managed by a controller, `kube-system` pods lacking a `PodDisruptionBudget` (or restricted by `maxUnavailable: 0`), pods with `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"`, and pods with local `emptyDir` storage unless annotated with `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: SAFE-TO-EVICT-TRUE-AND-PDB-FOR-SYSTEM-PODS",
          "cluster-autoscaler.kubernetes.io/safe-to-evict",
          "PodDisruptionBudget",
          "emptyDir",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C18: `cert-d5-01-cos-containerd-vs-ubuntu-sysctl` — Applying Linux kernel sysctls and kubelet config on COS_CONTAINERD node pools

- **1. Test Case ID & Title:** `cert-d5-01-cos-containerd-vs-ubuntu-sysctl` — _Applying Linux kernel sysctls and kubelet config on COS_CONTAINERD node pools_ ([task.yaml](gcp-gke-cert-suite/cert-d5-01-cos-containerd-vs-ubuntu-sysctl/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D5. Node OS, Kubelet & Auto-Repair` | **`domains.yaml`:** `cluster-debugging` | **Exam Source:** `GCP PCA / PCSE`
- **3. Target Skill:** `gke-workload-troubleshooting`
- **4. Scenario Prompt:** High-throughput proxy pods on our `COS_CONTAINERD` GKE node pool need node-level Linux kernel `sysctl` tuning (`net.core.somaxconn` and `net.ipv4.tcp_tw_reuse`) without privileged init containers. Which `gcloud container node-pools update` flag and YAML top-level section apply managed node `sysctls` on GKE? Start your answer with `VERDICT: SYSTEM-CONFIG-FROM-FILE-LINUXCONFIG-SYSCTLS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: SYSTEM-CONFIG-FROM-FILE-LINUXCONFIG-SYSCTLS. Pass `--system-config-from-file=<config.yaml>` to `gcloud container node-pools create` or `update` with a `linuxConfig.sysctls` map defining `net.core.somaxconn` and `net.ipv4.tcp_tw_reuse`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: SYSTEM-CONFIG-FROM-FILE-LINUXCONFIG-SYSCTLS', '--system-config-from-file', 'linuxConfig', 'sysctls']`

```yaml
# Certification Exam Domain Probe (GCP PCA / PCSE) — D5. Node OS, Kubelet & Auto-Repair
# Target skill: gke-workload-troubleshooting
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d5-01-cos-containerd-vs-ubuntu-sysctl
name: "Applying Linux kernel sysctls and kubelet config on COS_CONTAINERD node pools"
domain: cluster-debugging
owner: toshiowang
expected_fail: true

prompt: >-
  High-throughput proxy pods on our `COS_CONTAINERD` GKE node pool need node-level Linux kernel `sysctl` tuning (`net.core.somaxconn` and `net.ipv4.tcp_tw_reuse`) without privileged init containers. Which `gcloud container node-pools update` flag and YAML top-level section apply managed node `sysctls` on GKE? Start your answer with `VERDICT: SYSTEM-CONFIG-FROM-FILE-LINUXCONFIG-SYSCTLS`. Do not apply anything.
expected_output: >-
  VERDICT: SYSTEM-CONFIG-FROM-FILE-LINUXCONFIG-SYSCTLS. Pass `--system-config-from-file=<config.yaml>` to `gcloud container node-pools create` or `update` with a `linuxConfig.sysctls` map defining `net.core.somaxconn` and `net.ipv4.tcp_tw_reuse`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: SYSTEM-CONFIG-FROM-FILE-LINUXCONFIG-SYSCTLS",
          "--system-config-from-file",
          "linuxConfig",
          "sysctls",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C19: `cert-d5-02-static-pod-vs-daemonset-triage` — Identifying kubelet static mirror pods vs DaemonSet pods during node debugging

- **1. Test Case ID & Title:** `cert-d5-02-static-pod-vs-daemonset-triage` — _Identifying kubelet static mirror pods vs DaemonSet pods during node debugging_ ([task.yaml](gcp-gke-cert-suite/cert-d5-02-static-pod-vs-daemonset-triage/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D5. Node OS, Kubelet & Auto-Repair` | **`domains.yaml`:** `cluster-debugging` | **Exam Source:** `CNCF CKA`
- **3. Target Skill:** `gke-workload-troubleshooting`
- **4. Scenario Prompt:** An operator deletes a rogue pod named `rogue-agent-gke-pool-1-node-a` with `kubectl delete pod`, but it immediately reappears even though `kubectl get deploy,ds,rs,sts,job -A` shows zero controllers managing it and its `ownerReferences.kind` is `Node`. Explain what kind of pod this is, why the API server cannot stop it, and which kubelet directory on the node holds its manifest. Start your answer with `VERDICT: KUBELET-STATIC-MIRROR-POD-IN-ETC-KUBERNETES-MANIFESTS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: KUBELET-STATIC-MIRROR-POD-IN-ETC-KUBERNETES-MANIFESTS. A pod with `ownerReferences.kind: Node` and the node name suffixed is a static mirror pod managed directly by the node's `kubelet` process from `staticPodPath` (`/etc/kubernetes/manifests`), so deleting the mirror object in the API server causes `kubelet` to recreate it until the file is removed from the node.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: KUBELET-STATIC-MIRROR-POD-IN-ETC-KUBERNETES-MANIFESTS', '/etc/kubernetes/manifests', 'staticPodPath']`

```yaml
# Certification Exam Domain Probe (CNCF CKA) — D5. Node OS, Kubelet & Auto-Repair
# Target skill: gke-workload-troubleshooting
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d5-02-static-pod-vs-daemonset-triage
name: "Identifying kubelet static mirror pods vs DaemonSet pods during node debugging"
domain: cluster-debugging
owner: toshiowang
expected_fail: true

prompt: >-
  An operator deletes a rogue pod named `rogue-agent-gke-pool-1-node-a` with `kubectl delete pod`, but it immediately reappears even though `kubectl get deploy,ds,rs,sts,job -A` shows zero controllers managing it and its `ownerReferences.kind` is `Node`. Explain what kind of pod this is, why the API server cannot stop it, and which kubelet directory on the node holds its manifest. Start your answer with `VERDICT: KUBELET-STATIC-MIRROR-POD-IN-ETC-KUBERNETES-MANIFESTS`. Do not apply anything.
expected_output: >-
  VERDICT: KUBELET-STATIC-MIRROR-POD-IN-ETC-KUBERNETES-MANIFESTS. A pod with `ownerReferences.kind: Node` and the node name suffixed is a static mirror pod managed directly by the node's `kubelet` process from `staticPodPath` (`/etc/kubernetes/manifests`), so deleting the mirror object in the API server causes `kubelet` to recreate it until the file is removed from the node.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: KUBELET-STATIC-MIRROR-POD-IN-ETC-KUBERNETES-MANIFESTS",
          "/etc/kubernetes/manifests",
          "staticPodPath",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C20: `cert-d5-03-noexecute-taint-toleration-seconds` — Controlling pod eviction timing on NotReady nodes with NoExecute tolerationSeconds

- **1. Test Case ID & Title:** `cert-d5-03-noexecute-taint-toleration-seconds` — _Controlling pod eviction timing on NotReady nodes with NoExecute tolerationSeconds_ ([task.yaml](gcp-gke-cert-suite/cert-d5-03-noexecute-taint-toleration-seconds/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D5. Node OS, Kubelet & Auto-Repair` | **`domains.yaml`:** `cluster-debugging` | **Exam Source:** `CNCF CKA`
- **3. Target Skill:** `gke-reliability`
- **4. Scenario Prompt:** By default Kubernetes waits 300 seconds before evicting pods from a node tainted with `node.kubernetes.io/not-ready:NoExecute` or `node.kubernetes.io/unreachable:NoExecute`. Our stateful payment gateway needs pods evicted within 30 seconds of a node becoming unreachable so volumes reattach faster. Which pod `tolerations` fields override the 300s default down to 30s? Start your answer with `VERDICT: NOEXECUTE-TOLERATION-WITH-TOLERATIONSECONDS-30`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: NOEXECUTE-TOLERATION-WITH-TOLERATIONSECONDS-30. Add explicit `tolerations` for keys `node.kubernetes.io/not-ready` and `node.kubernetes.io/unreachable` with `operator: Exists`, `effect: NoExecute`, and `tolerationSeconds: 30`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: NOEXECUTE-TOLERATION-WITH-TOLERATIONSECONDS-30', 'node.kubernetes.io/unreachable', 'NoExecute', 'tolerationSeconds']`

```yaml
# Certification Exam Domain Probe (CNCF CKA) — D5. Node OS, Kubelet & Auto-Repair
# Target skill: gke-reliability
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d5-03-noexecute-taint-toleration-seconds
name: "Controlling pod eviction timing on NotReady nodes with NoExecute tolerationSeconds"
domain: cluster-debugging
owner: toshiowang
expected_fail: true

prompt: >-
  By default Kubernetes waits 300 seconds before evicting pods from a node tainted with `node.kubernetes.io/not-ready:NoExecute` or `node.kubernetes.io/unreachable:NoExecute`. Our stateful payment gateway needs pods evicted within 30 seconds of a node becoming unreachable so volumes reattach faster. Which pod `tolerations` fields override the 300s default down to 30s? Start your answer with `VERDICT: NOEXECUTE-TOLERATION-WITH-TOLERATIONSECONDS-30`. Do not apply anything.
expected_output: >-
  VERDICT: NOEXECUTE-TOLERATION-WITH-TOLERATIONSECONDS-30. Add explicit `tolerations` for keys `node.kubernetes.io/not-ready` and `node.kubernetes.io/unreachable` with `operator: Exists`, `effect: NoExecute`, and `tolerationSeconds: 30`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: NOEXECUTE-TOLERATION-WITH-TOLERATIONSECONDS-30",
          "node.kubernetes.io/unreachable",
          "NoExecute",
          "tolerationSeconds",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C21: `cert-d6-01-shared-vpc-host-iam-bindings` — Shared VPC host project subnet IAM bindings for GKE service project agents

- **1. Test Case ID & Title:** `cert-d6-01-shared-vpc-host-iam-bindings` — _Shared VPC host project subnet IAM bindings for GKE service project agents_ ([task.yaml](gcp-gke-cert-suite/cert-d6-01-shared-vpc-host-iam-bindings/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCNE / PCA`
- **3. Target Skill:** `gke-networking`
- **4. Scenario Prompt:** Provisioning a VPC-native GKE cluster in service project `app-svc-proj` (project number `111122223333`) attached to a subnet in Shared VPC host project `net-host-proj` fails with a permission error on the host subnet. Which IAM role on the host project/subnet must be granted to the service project's GKE service agent (`service-111122223333@container-engine-robot.iam.gserviceaccount.com`) and Google APIs service agent (`111122223333@cloudservices.gserviceaccount.com`)? Start your answer with `VERDICT: GRANT-COMPUTE-NETWORKUSER-ON-HOST-SUBNET`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: GRANT-COMPUTE-NETWORKUSER-ON-HOST-SUBNET. Grant `roles/compute.networkUser` on the Shared VPC host project subnet (and secondary Pod/Service ranges) to both `service-111122223333@container-engine-robot.iam.gserviceaccount.com` and `111122223333@cloudservices.gserviceaccount.com` (plus `roles/container.hostServiceAgentUser` at the host project level for the GKE robot account).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: GRANT-COMPUTE-NETWORKUSER-ON-HOST-SUBNET', 'roles/compute.networkUser', 'container-engine-robot.iam.gserviceaccount.com', 'roles/container.hostServiceAgentUser']`

```yaml
# Certification Exam Domain Probe (GCP PCNE / PCA) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-01-shared-vpc-host-iam-bindings
name: "Shared VPC host project subnet IAM bindings for GKE service project agents"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  Provisioning a VPC-native GKE cluster in service project `app-svc-proj` (project number `111122223333`) attached to a subnet in Shared VPC host project `net-host-proj` fails with a permission error on the host subnet. Which IAM role on the host project/subnet must be granted to the service project's GKE service agent (`service-111122223333@container-engine-robot.iam.gserviceaccount.com`) and Google APIs service agent (`111122223333@cloudservices.gserviceaccount.com`)? Start your answer with `VERDICT: GRANT-COMPUTE-NETWORKUSER-ON-HOST-SUBNET`. Do not apply anything.
expected_output: >-
  VERDICT: GRANT-COMPUTE-NETWORKUSER-ON-HOST-SUBNET. Grant `roles/compute.networkUser` on the Shared VPC host project subnet (and secondary Pod/Service ranges) to both `service-111122223333@container-engine-robot.iam.gserviceaccount.com` and `111122223333@cloudservices.gserviceaccount.com` (plus `roles/container.hostServiceAgentUser` at the host project level for the GKE robot account).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: GRANT-COMPUTE-NETWORKUSER-ON-HOST-SUBNET",
          "roles/compute.networkUser",
          "container-engine-robot.iam.gserviceaccount.com",
          "roles/container.hostServiceAgentUser",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C22: `cert-d6-02-gateway-api-cross-namespace-refgrant` — GKE Gateway API cross-namespace HTTPRoute to Service ReferenceGrant

- **1. Test Case ID & Title:** `cert-d6-02-gateway-api-cross-namespace-refgrant` — _GKE Gateway API cross-namespace HTTPRoute to Service ReferenceGrant_ ([task.yaml](gcp-gke-cert-suite/cert-d6-02-gateway-api-cross-namespace-refgrant/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `cluster-debugging` | **Exam Source:** `GCP PCNE / PCA`
- **3. Target Skill:** `gke-service-networking`
- **4. Scenario Prompt:** An `HTTPRoute` in namespace `edge-routing` references `Service/billing-api` in namespace `billing-prod`, and `kubectl describe httproute` shows `ResolvedRefs: False` with reason `RefNotPermitted`. Which Gateway API resource must be created, in which namespace (`edge-routing` or `billing-prod`), and what `from` / `to` kinds must it declare? Start your answer with `VERDICT: CREATE-REFERENCEGRANT-IN-TARGET-NAMESPACE-BILLING-PROD`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: CREATE-REFERENCEGRANT-IN-TARGET-NAMESPACE-BILLING-PROD. Create a `ReferenceGrant` (`gateway.networking.k8s.io/v1beta1`) in the target namespace `billing-prod` allowing `from: [{group: gateway.networking.k8s.io, kind: HTTPRoute, namespace: edge-routing}]` and `to: [{group: "", kind: Service, name: billing-api}]`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: CREATE-REFERENCEGRANT-IN-TARGET-NAMESPACE-BILLING-PROD', 'ReferenceGrant', 'gateway.networking.k8s.io', 'billing-prod']`

```yaml
# Certification Exam Domain Probe (GCP PCNE / PCA) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-service-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-02-gateway-api-cross-namespace-refgrant
name: "GKE Gateway API cross-namespace HTTPRoute to Service ReferenceGrant"
domain: cluster-debugging
owner: toshiowang
expected_fail: true

prompt: >-
  An `HTTPRoute` in namespace `edge-routing` references `Service/billing-api` in namespace `billing-prod`, and `kubectl describe httproute` shows `ResolvedRefs: False` with reason `RefNotPermitted`. Which Gateway API resource must be created, in which namespace (`edge-routing` or `billing-prod`), and what `from` / `to` kinds must it declare? Start your answer with `VERDICT: CREATE-REFERENCEGRANT-IN-TARGET-NAMESPACE-BILLING-PROD`. Do not apply anything.
expected_output: >-
  VERDICT: CREATE-REFERENCEGRANT-IN-TARGET-NAMESPACE-BILLING-PROD. Create a `ReferenceGrant` (`gateway.networking.k8s.io/v1beta1`) in the target namespace `billing-prod` allowing `from: [{group: gateway.networking.k8s.io, kind: HTTPRoute, namespace: edge-routing}]` and `to: [{group: "", kind: Service, name: billing-api}]`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: CREATE-REFERENCEGRANT-IN-TARGET-NAMESPACE-BILLING-PROD",
          "ReferenceGrant",
          "gateway.networking.k8s.io",
          "billing-prod",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C23: `cert-d6-03-gateway-healthcheckpolicy-port` — Resolving GKE Gateway 502 Bad Gateway errors with a HealthCheckPolicy CRD

- **1. Test Case ID & Title:** `cert-d6-03-gateway-healthcheckpolicy-port` — _Resolving GKE Gateway 502 Bad Gateway errors with a HealthCheckPolicy CRD_ ([task.yaml](gcp-gke-cert-suite/cert-d6-03-gateway-healthcheckpolicy-port/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `cluster-debugging` | **Exam Source:** `GCP PCNE`
- **3. Target Skill:** `gke-service-networking`
- **4. Scenario Prompt:** Traffic through our GKE Gateway (`gke-l7-regional-external-managed`) to `Service/catalog-svc` (Service port `80` -> container `targetPort: 8080`) returns `502 Bad Gateway` because the application exposes its health probe at `/actuator/health` on management port `8081` rather than `/` on `8080`. Which GKE Gateway API policy CRD (`networking.gke.io/v1`) overrides the load balancer health check path and port for `Service/catalog-svc`? Start your answer with `VERDICT: ATTACH-HEALTHCHECKPOLICY-TO-CATALOG-SVC`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ATTACH-HEALTHCHECKPOLICY-TO-CATALOG-SVC. Create a `HealthCheckPolicy` (`apiVersion: networking.gke.io/v1`) with `spec.targetRef` pointing to `Service/catalog-svc` and `spec.default.config` configuring `port: 8081` and `httpHealthCheck.requestPath: /actuator/health`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ATTACH-HEALTHCHECKPOLICY-TO-CATALOG-SVC', 'HealthCheckPolicy', 'networking.gke.io/v1', 'targetRef']`

```yaml
# Certification Exam Domain Probe (GCP PCNE) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-service-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-03-gateway-healthcheckpolicy-port
name: "Resolving GKE Gateway 502 Bad Gateway errors with a HealthCheckPolicy CRD"
domain: cluster-debugging
owner: toshiowang
expected_fail: true

prompt: >-
  Traffic through our GKE Gateway (`gke-l7-regional-external-managed`) to `Service/catalog-svc` (Service port `80` -> container `targetPort: 8080`) returns `502 Bad Gateway` because the application exposes its health probe at `/actuator/health` on management port `8081` rather than `/` on `8080`. Which GKE Gateway API policy CRD (`networking.gke.io/v1`) overrides the load balancer health check path and port for `Service/catalog-svc`? Start your answer with `VERDICT: ATTACH-HEALTHCHECKPOLICY-TO-CATALOG-SVC`. Do not apply anything.
expected_output: >-
  VERDICT: ATTACH-HEALTHCHECKPOLICY-TO-CATALOG-SVC. Create a `HealthCheckPolicy` (`apiVersion: networking.gke.io/v1`) with `spec.targetRef` pointing to `Service/catalog-svc` and `spec.default.config` configuring `port: 8081` and `httpHealthCheck.requestPath: /actuator/health`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ATTACH-HEALTHCHECKPOLICY-TO-CATALOG-SVC",
          "HealthCheckPolicy",
          "networking.gke.io/v1",
          "targetRef",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C24: `cert-d6-04-dataplane-v2-egress-dns-policy` — Permitting kube-dns and NodeLocal DNSCache under a default-deny egress NetworkPolicy

- **1. Test Case ID & Title:** `cert-d6-04-dataplane-v2-egress-dns-policy` — _Permitting kube-dns and NodeLocal DNSCache under a default-deny egress NetworkPolicy_ ([task.yaml](gcp-gke-cert-suite/cert-d6-04-dataplane-v2-egress-dns-policy/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `security` | **Exam Source:** `GCP PCNE / CNCF CKS`
- **3. Target Skill:** `gke-networking`
- **4. Scenario Prompt:** After applying a default-deny egress `NetworkPolicy` in namespace `payments`, pods time out resolving both cluster-internal Services and external FQDNs on our GKE Dataplane V2 cluster with NodeLocal DNSCache enabled. What egress rules (ports, protocols, namespace/pod selectors, and link-local IP) must be added to allow DNS lookups? Start your answer with `VERDICT: ALLOW-UDP-TCP-53-TO-KUBE-DNS-AND-NODELOCAL-DNS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ALLOW-UDP-TCP-53-TO-KUBE-DNS-AND-NODELOCAL-DNS. Add an egress rule allowing `UDP` and `TCP` port `53` (and port `8053` where applicable) to `namespaceSelector` `kubernetes.io/metadata.name: kube-system` with `podSelector` `k8s-app: kube-dns` as well as the NodeLocal DNSCache link-local address.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ALLOW-UDP-TCP-53-TO-KUBE-DNS-AND-NODELOCAL-DNS', 'kube-dns', 'kube-system', '53']`

```yaml
# Certification Exam Domain Probe (GCP PCNE / CNCF CKS) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-04-dataplane-v2-egress-dns-policy
name: "Permitting kube-dns and NodeLocal DNSCache under a default-deny egress NetworkPolicy"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  After applying a default-deny egress `NetworkPolicy` in namespace `payments`, pods time out resolving both cluster-internal Services and external FQDNs on our GKE Dataplane V2 cluster with NodeLocal DNSCache enabled. What egress rules (ports, protocols, namespace/pod selectors, and link-local IP) must be added to allow DNS lookups? Start your answer with `VERDICT: ALLOW-UDP-TCP-53-TO-KUBE-DNS-AND-NODELOCAL-DNS`. Do not apply anything.
expected_output: >-
  VERDICT: ALLOW-UDP-TCP-53-TO-KUBE-DNS-AND-NODELOCAL-DNS. Add an egress rule allowing `UDP` and `TCP` port `53` (and port `8053` where applicable) to `namespaceSelector` `kubernetes.io/metadata.name: kube-system` with `podSelector` `k8s-app: kube-dns` as well as the NodeLocal DNSCache link-local address.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ALLOW-UDP-TCP-53-TO-KUBE-DNS-AND-NODELOCAL-DNS",
          "kube-dns",
          "kube-system",
          "53",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C25: `cert-d6-05-cloud-nat-port-exhaustion-dpa` — Resolving Cloud NAT ephemeral port exhaustion on GKE with Dynamic Port Allocation

- **1. Test Case ID & Title:** `cert-d6-05-cloud-nat-port-exhaustion-dpa` — _Resolving Cloud NAT ephemeral port exhaustion on GKE with Dynamic Port Allocation_ ([task.yaml](gcp-gke-cert-suite/cert-d6-05-cloud-nat-port-exhaustion-dpa/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `capacity` | **Exam Source:** `GCP PCNE`
- **3. Target Skill:** `gke-networking`
- **4. Scenario Prompt:** Private GKE nodes making thousands of concurrent outbound HTTPS connections to a partner API experience intermittent connection timeouts, and Cloud NAT logs report `OUT_OF_RESOURCES` port allocation drops even though most nodes in the cluster are idle. Give the exact `gcloud compute routers nats update` flags to enable Dynamic Port Allocation and disable Endpoint-Independent Mapping. Start your answer with `VERDICT: ENABLE-DYNAMIC-PORT-ALLOCATION-ON-CLOUD-NAT`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ENABLE-DYNAMIC-PORT-ALLOCATION-ON-CLOUD-NAT. Run `gcloud compute routers nats update <nat-name> --router=<router> --region=<region> --enable-dynamic-port-allocation --min-ports-per-vm=<min> --max-ports-per-vm=<max> --enable-endpoint-independent-mapping=false`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ENABLE-DYNAMIC-PORT-ALLOCATION-ON-CLOUD-NAT', '--enable-dynamic-port-allocation', '--max-ports-per-vm']`

```yaml
# Certification Exam Domain Probe (GCP PCNE) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-05-cloud-nat-port-exhaustion-dpa
name: "Resolving Cloud NAT ephemeral port exhaustion on GKE with Dynamic Port Allocation"
domain: capacity
owner: toshiowang
expected_fail: true

prompt: >-
  Private GKE nodes making thousands of concurrent outbound HTTPS connections to a partner API experience intermittent connection timeouts, and Cloud NAT logs report `OUT_OF_RESOURCES` port allocation drops even though most nodes in the cluster are idle. Give the exact `gcloud compute routers nats update` flags to enable Dynamic Port Allocation and disable Endpoint-Independent Mapping. Start your answer with `VERDICT: ENABLE-DYNAMIC-PORT-ALLOCATION-ON-CLOUD-NAT`. Do not apply anything.
expected_output: >-
  VERDICT: ENABLE-DYNAMIC-PORT-ALLOCATION-ON-CLOUD-NAT. Run `gcloud compute routers nats update <nat-name> --router=<router> --region=<region> --enable-dynamic-port-allocation --min-ports-per-vm=<min> --max-ports-per-vm=<max> --enable-endpoint-independent-mapping=false`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ENABLE-DYNAMIC-PORT-ALLOCATION-ON-CLOUD-NAT",
          "--enable-dynamic-port-allocation",
          "--max-ports-per-vm",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C26: `cert-d6-06-container-native-lb-neg-client-ip` — Container-Native Load Balancing (NEGs) and externalTrafficPolicy Local for client IP preservation

- **1. Test Case ID & Title:** `cert-d6-06-container-native-lb-neg-client-ip` — _Container-Native Load Balancing (NEGs) and externalTrafficPolicy Local for client IP preservation_ ([task.yaml](gcp-gke-cert-suite/cert-d6-06-container-native-lb-neg-client-ip/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCNE / PCA`
- **3. Target Skill:** `gke-service-networking`
- **4. Scenario Prompt:** Our GKE Service behind an external Application Load Balancer sees node internal IPs instead of client source IPs and suffers extra latency from double-hop `kube-proxy` iptables routing across nodes. Which Service annotation enables direct pod-IP routing via Network Endpoint Groups (NEGs) on GKE, and which `Service.spec` field preserves client source IP on NodePort / LoadBalancer Services? Start your answer with `VERDICT: USE-CLOUD-GOOGLE-COM-NEG-AND-LOCAL-TRAFFIC-POLICY`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: USE-CLOUD-GOOGLE-COM-NEG-AND-LOCAL-TRAFFIC-POLICY. Annotate the Service with `cloud.google.com/neg: '{"ingress": true}'` so the load balancer routes directly to Pod IPs via standalone/ingress `NetworkEndpointGroup` backends, or set `externalTrafficPolicy: Local` for passthrough LoadBalancer/NodePort Services.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: USE-CLOUD-GOOGLE-COM-NEG-AND-LOCAL-TRAFFIC-POLICY', 'cloud.google.com/neg', 'externalTrafficPolicy: Local']`

```yaml
# Certification Exam Domain Probe (GCP PCNE / PCA) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-service-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-06-container-native-lb-neg-client-ip
name: "Container-Native Load Balancing (NEGs) and externalTrafficPolicy Local for client IP preservation"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  Our GKE Service behind an external Application Load Balancer sees node internal IPs instead of client source IPs and suffers extra latency from double-hop `kube-proxy` iptables routing across nodes. Which Service annotation enables direct pod-IP routing via Network Endpoint Groups (NEGs) on GKE, and which `Service.spec` field preserves client source IP on NodePort / LoadBalancer Services? Start your answer with `VERDICT: USE-CLOUD-GOOGLE-COM-NEG-AND-LOCAL-TRAFFIC-POLICY`. Do not apply anything.
expected_output: >-
  VERDICT: USE-CLOUD-GOOGLE-COM-NEG-AND-LOCAL-TRAFFIC-POLICY. Annotate the Service with `cloud.google.com/neg: '{"ingress": true}'` so the load balancer routes directly to Pod IPs via standalone/ingress `NetworkEndpointGroup` backends, or set `externalTrafficPolicy: Local` for passthrough LoadBalancer/NodePort Services.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: USE-CLOUD-GOOGLE-COM-NEG-AND-LOCAL-TRAFFIC-POLICY",
          "cloud.google.com/neg",
          "externalTrafficPolicy: Local",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C27: `cert-d6-07-internal-passthrough-nlb-all-ports` — GKE Internal Passthrough Network Load Balancer annotations and global access

- **1. Test Case ID & Title:** `cert-d6-07-internal-passthrough-nlb-all-ports` — _GKE Internal Passthrough Network Load Balancer annotations and global access_ ([task.yaml](gcp-gke-cert-suite/cert-d6-07-internal-passthrough-nlb-all-ports/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCNE`
- **3. Target Skill:** `gke-service-networking`
- **4. Scenario Prompt:** Clients in `us-west1` and `us-central1` on the same VPC need to reach a `type: LoadBalancer` Service on our GKE cluster in `us-central1` over a RFC 1918 internal IP without traversing the public internet. Give the two exact GKE Service annotations (`networking.gke.io/*`) that provision an internal passthrough Network Load Balancer and allow clients in any region to reach it. Start your answer with `VERDICT: INTERNAL-LB-ANNOTATION-WITH-GLOBAL-ACCESS`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: INTERNAL-LB-ANNOTATION-WITH-GLOBAL-ACCESS. Add Service annotations `networking.gke.io/load-balancer-type: "Internal"` and `networking.gke.io/internal-load-balancer-allow-global-access: "true"`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: INTERNAL-LB-ANNOTATION-WITH-GLOBAL-ACCESS', 'networking.gke.io/load-balancer-type', 'networking.gke.io/internal-load-balancer-allow-global-access']`

```yaml
# Certification Exam Domain Probe (GCP PCNE) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-service-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-07-internal-passthrough-nlb-all-ports
name: "GKE Internal Passthrough Network Load Balancer annotations and global access"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  Clients in `us-west1` and `us-central1` on the same VPC need to reach a `type: LoadBalancer` Service on our GKE cluster in `us-central1` over a RFC 1918 internal IP without traversing the public internet. Give the two exact GKE Service annotations (`networking.gke.io/*`) that provision an internal passthrough Network Load Balancer and allow clients in any region to reach it. Start your answer with `VERDICT: INTERNAL-LB-ANNOTATION-WITH-GLOBAL-ACCESS`. Do not apply anything.
expected_output: >-
  VERDICT: INTERNAL-LB-ANNOTATION-WITH-GLOBAL-ACCESS. Add Service annotations `networking.gke.io/load-balancer-type: "Internal"` and `networking.gke.io/internal-load-balancer-allow-global-access: "true"`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: INTERNAL-LB-ANNOTATION-WITH-GLOBAL-ACCESS",
          "networking.gke.io/load-balancer-type",
          "networking.gke.io/internal-load-balancer-allow-global-access",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C28: `cert-d6-08-nodelocal-dnscache-enablement` — Enabling GKE NodeLocal DNSCache add-on to prevent DNS conntrack races and 5s timeouts

- **1. Test Case ID & Title:** `cert-d6-08-nodelocal-dnscache-enablement` — _Enabling GKE NodeLocal DNSCache add-on to prevent DNS conntrack races and 5s timeouts_ ([task.yaml](gcp-gke-cert-suite/cert-d6-08-nodelocal-dnscache-enablement/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D6. Networking, CNI, LBs & DNS` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCNE / PCDE`
- **3. Target Skill:** `gke-networking`
- **4. Scenario Prompt:** High-QPS microservices on our GKE Standard cluster experience intermittent 5-second DNS lookup delays and `nf_conntrack` table spikes from UDP DNS queries to `kube-dns`. Give the exact `gcloud container clusters update` flag to enable the managed local DNS caching DaemonSet on the cluster. Start your answer with `VERDICT: UPDATE-ADDONS-NODELOCALDNS-ENABLED`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: UPDATE-ADDONS-NODELOCALDNS-ENABLED. Run `gcloud container clusters update <cluster> --location=<location> --update-addons=NodeLocalDNS=ENABLED` to deploy the `node-local-dns` DaemonSet (`NodeLocal DNSCache`), which caches DNS responses locally on each node and upgrades upstream cache misses to TCP.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: UPDATE-ADDONS-NODELOCALDNS-ENABLED', '--update-addons=NodeLocalDNS=ENABLED', 'node-local-dns']`

```yaml
# Certification Exam Domain Probe (GCP PCNE / PCDE) — D6. Networking, CNI, LBs & DNS
# Target skill: gke-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d6-08-nodelocal-dnscache-enablement
name: "Enabling GKE NodeLocal DNSCache add-on to prevent DNS conntrack races and 5s timeouts"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  High-QPS microservices on our GKE Standard cluster experience intermittent 5-second DNS lookup delays and `nf_conntrack` table spikes from UDP DNS queries to `kube-dns`. Give the exact `gcloud container clusters update` flag to enable the managed local DNS caching DaemonSet on the cluster. Start your answer with `VERDICT: UPDATE-ADDONS-NODELOCALDNS-ENABLED`. Do not apply anything.
expected_output: >-
  VERDICT: UPDATE-ADDONS-NODELOCALDNS-ENABLED. Run `gcloud container clusters update <cluster> --location=<location> --update-addons=NodeLocalDNS=ENABLED` to deploy the `node-local-dns` DaemonSet (`NodeLocal DNSCache`), which caches DNS responses locally on each node and upgrades upstream cache misses to TCP.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: UPDATE-ADDONS-NODELOCALDNS-ENABLED",
          "--update-addons=NodeLocalDNS=ENABLED",
          "node-local-dns",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C29: `cert-d7-01-binary-authorization-attestor-policy` — Binary Authorization REQUIRE_ATTESTATION policy and breakglass audit trail

- **1. Test Case ID & Title:** `cert-d7-01-binary-authorization-attestor-policy` — _Binary Authorization REQUIRE_ATTESTATION policy and breakglass audit trail_ ([task.yaml](gcp-gke-cert-suite/cert-d7-01-binary-authorization-attestor-policy/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `GCP PCSE / PCDE`
- **3. Target Skill:** `gke-platform-security`
- **4. Scenario Prompt:** Security compliance requires our GKE cluster to reject any container image not signed by our Cloud Build vulnerability-scan attestor, while still allowing an on-call SRE to deploy an unsigned hotfix pod during a P0 incident with an automatic Cloud Audit Log trail. Which Binary Authorization evaluation mode enforces attestations, and which pod label/annotation invokes emergency breakglass? Start your answer with `VERDICT: REQUIRE-ATTESTATION-WITH-BREAK-GLASS-ANNOTATION`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: REQUIRE-ATTESTATION-WITH-BREAK-GLASS-ANNOTATION. Set Binary Authorization policy `evaluationMode: REQUIRE_ATTESTATION` (`--binauthz-evaluation-mode=PROJECT_SINGLETON_POLICY_ENFORCE`) and use the pod annotation `alpha.image-policy.k8s.io/break-glass: "true"` (or `image-policy.k8s.io/break-glass`) for audited emergency deployments.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: REQUIRE-ATTESTATION-WITH-BREAK-GLASS-ANNOTATION', 'REQUIRE_ATTESTATION', 'break-glass']`

```yaml
# Certification Exam Domain Probe (GCP PCSE / PCDE) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-platform-security
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-01-binary-authorization-attestor-policy
name: "Binary Authorization REQUIRE_ATTESTATION policy and breakglass audit trail"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  Security compliance requires our GKE cluster to reject any container image not signed by our Cloud Build vulnerability-scan attestor, while still allowing an on-call SRE to deploy an unsigned hotfix pod during a P0 incident with an automatic Cloud Audit Log trail. Which Binary Authorization evaluation mode enforces attestations, and which pod label/annotation invokes emergency breakglass? Start your answer with `VERDICT: REQUIRE-ATTESTATION-WITH-BREAK-GLASS-ANNOTATION`. Do not apply anything.
expected_output: >-
  VERDICT: REQUIRE-ATTESTATION-WITH-BREAK-GLASS-ANNOTATION. Set Binary Authorization policy `evaluationMode: REQUIRE_ATTESTATION` (`--binauthz-evaluation-mode=PROJECT_SINGLETON_POLICY_ENFORCE`) and use the pod annotation `alpha.image-policy.k8s.io/break-glass: "true"` (or `image-policy.k8s.io/break-glass`) for audited emergency deployments.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: REQUIRE-ATTESTATION-WITH-BREAK-GLASS-ANNOTATION",
          "REQUIRE_ATTESTATION",
          "break-glass",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C30: `cert-d7-02-vpc-service-controls-egress-block` — Diagnosing and resolving VPC Service Controls perimeter blocks on GKE image pulls

- **1. Test Case ID & Title:** `cert-d7-02-vpc-service-controls-egress-block` — _Diagnosing and resolving VPC Service Controls perimeter blocks on GKE image pulls_ ([task.yaml](gcp-gke-cert-suite/cert-d7-02-vpc-service-controls-egress-block/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `GCP PCSE`
- **3. Target Skill:** `gke-platform-security`
- **4. Scenario Prompt:** Pods in our GKE cluster inside VPC Service Controls perimeter `prod-perimeter` fail to pull container images from a shared Artifact Registry in project `shared-artifacts-proj` (outside `prod-perimeter`), and Cloud Audit Logs show `violationReason: RESOURCES_NOT_IN_SAME_SERVICE_PERIMETER` on `artifactregistry.googleapis.com`. What VPC Service Controls configuration on `prod-perimeter` permits the GKE node/workload service account to pull from `shared-artifacts-proj` without disabling the perimeter? Start your answer with `VERDICT: CONFIGURE-VPCSC-EGRESS-RULE-OR-PERIMETER-BRIDGE`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: CONFIGURE-VPCSC-EGRESS-RULE-OR-PERIMETER-BRIDGE. Add a VPC Service Controls egress rule on `prod-perimeter` allowing the GKE node/Workload Identity principal to access `artifactregistry.googleapis.com` and `storage.googleapis.com` in `shared-artifacts-proj` (or create a Perimeter Bridge if both projects belong to perimeters under the same organization).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: CONFIGURE-VPCSC-EGRESS-RULE-OR-PERIMETER-BRIDGE', 'artifactregistry.googleapis.com', 'egress', 'VPC Service Controls']`

```yaml
# Certification Exam Domain Probe (GCP PCSE) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-platform-security
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-02-vpc-service-controls-egress-block
name: "Diagnosing and resolving VPC Service Controls perimeter blocks on GKE image pulls"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  Pods in our GKE cluster inside VPC Service Controls perimeter `prod-perimeter` fail to pull container images from a shared Artifact Registry in project `shared-artifacts-proj` (outside `prod-perimeter`), and Cloud Audit Logs show `violationReason: RESOURCES_NOT_IN_SAME_SERVICE_PERIMETER` on `artifactregistry.googleapis.com`. What VPC Service Controls configuration on `prod-perimeter` permits the GKE node/workload service account to pull from `shared-artifacts-proj` without disabling the perimeter? Start your answer with `VERDICT: CONFIGURE-VPCSC-EGRESS-RULE-OR-PERIMETER-BRIDGE`. Do not apply anything.
expected_output: >-
  VERDICT: CONFIGURE-VPCSC-EGRESS-RULE-OR-PERIMETER-BRIDGE. Add a VPC Service Controls egress rule on `prod-perimeter` allowing the GKE node/Workload Identity principal to access `artifactregistry.googleapis.com` and `storage.googleapis.com` in `shared-artifacts-proj` (or create a Perimeter Bridge if both projects belong to perimeters under the same organization).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: CONFIGURE-VPCSC-EGRESS-RULE-OR-PERIMETER-BRIDGE",
          "artifactregistry.googleapis.com",
          "egress",
          "VPC Service Controls",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C31: `cert-d7-03-gke-sandbox-gvisor-runtimeclass` — Isolating untrusted workloads with GKE Sandbox (gVisor) RuntimeClass

- **1. Test Case ID & Title:** `cert-d7-03-gke-sandbox-gvisor-runtimeclass` — _Isolating untrusted workloads with GKE Sandbox (gVisor) RuntimeClass_ ([task.yaml](gcp-gke-cert-suite/cert-d7-03-gke-sandbox-gvisor-runtimeclass/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `GCP PCSE / CNCF CKS`
- **3. Target Skill:** `gke-workload-security`
- **4. Scenario Prompt:** We run third-party user-submitted code on GKE and need kernel-level syscall isolation so a container escape cannot compromise the host Linux kernel. Give the `gcloud container node-pools create` flag to enable GKE Sandbox on a node pool and the exact `Pod.spec` field/value a workload sets to run inside the sandbox. Start your answer with `VERDICT: SANDBOX-TYPE-GVISOR-AND-RUNTIMECLASSNAME-GVISOR`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: SANDBOX-TYPE-GVISOR-AND-RUNTIMECLASSNAME-GVISOR. Create the node pool with `--sandbox type=gvisor` (`--image-type=COS_CONTAINERD`) and set `runtimeClassName: gvisor` in the Pod `spec`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: SANDBOX-TYPE-GVISOR-AND-RUNTIMECLASSNAME-GVISOR', '--sandbox', 'runtimeClassName: gvisor']`

```yaml
# Certification Exam Domain Probe (GCP PCSE / CNCF CKS) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-workload-security
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-03-gke-sandbox-gvisor-runtimeclass
name: "Isolating untrusted workloads with GKE Sandbox (gVisor) RuntimeClass"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  We run third-party user-submitted code on GKE and need kernel-level syscall isolation so a container escape cannot compromise the host Linux kernel. Give the `gcloud container node-pools create` flag to enable GKE Sandbox on a node pool and the exact `Pod.spec` field/value a workload sets to run inside the sandbox. Start your answer with `VERDICT: SANDBOX-TYPE-GVISOR-AND-RUNTIMECLASSNAME-GVISOR`. Do not apply anything.
expected_output: >-
  VERDICT: SANDBOX-TYPE-GVISOR-AND-RUNTIMECLASSNAME-GVISOR. Create the node pool with `--sandbox type=gvisor` (`--image-type=COS_CONTAINERD`) and set `runtimeClassName: gvisor` in the Pod `spec`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: SANDBOX-TYPE-GVISOR-AND-RUNTIMECLASSNAME-GVISOR",
          "--sandbox",
          "runtimeClassName: gvisor",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C32: `cert-d7-04-pod-security-standards-restricted` — Remediating Pod securityContext to pass Pod Security Admission restricted profile

- **1. Test Case ID & Title:** `cert-d7-04-pod-security-standards-restricted` — _Remediating Pod securityContext to pass Pod Security Admission restricted profile_ ([task.yaml](gcp-gke-cert-suite/cert-d7-04-pod-security-standards-restricted/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `CNCF CKS / GCP PCSE`
- **3. Target Skill:** `gke-workload-security`
- **4. Scenario Prompt:** Namespace `regulated-apps` carries label `pod-security.kubernetes.io/enforce: restricted`, and a Deployment with an empty `securityContext: {}` is rejected at admission. List the four required `securityContext` fields/values (pod and container level) required for a Linux pod to pass the Kubernetes `restricted` Pod Security Standard. Start your answer with `VERDICT: NONROOT-NO-PRIV-ESCALATION-DROP-ALL-CAPS-SECCOMP-RUNTIMEDEFAULT`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: NONROOT-NO-PRIV-ESCALATION-DROP-ALL-CAPS-SECCOMP-RUNTIMEDEFAULT. Set `securityContext.runAsNonRoot: true`, `securityContext.seccompProfile.type: RuntimeDefault` (or `Localhost`), `securityContext.allowPrivilegeEscalation: false`, and `securityContext.capabilities.drop: ["ALL"]`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: NONROOT-NO-PRIV-ESCALATION-DROP-ALL-CAPS-SECCOMP-RUNTIMEDEFAULT', 'runAsNonRoot: true', 'allowPrivilegeEscalation: false', 'RuntimeDefault']`

```yaml
# Certification Exam Domain Probe (CNCF CKS / GCP PCSE) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-workload-security
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-04-pod-security-standards-restricted
name: "Remediating Pod securityContext to pass Pod Security Admission restricted profile"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  Namespace `regulated-apps` carries label `pod-security.kubernetes.io/enforce: restricted`, and a Deployment with an empty `securityContext: {}` is rejected at admission. List the four required `securityContext` fields/values (pod and container level) required for a Linux pod to pass the Kubernetes `restricted` Pod Security Standard. Start your answer with `VERDICT: NONROOT-NO-PRIV-ESCALATION-DROP-ALL-CAPS-SECCOMP-RUNTIMEDEFAULT`. Do not apply anything.
expected_output: >-
  VERDICT: NONROOT-NO-PRIV-ESCALATION-DROP-ALL-CAPS-SECCOMP-RUNTIMEDEFAULT. Set `securityContext.runAsNonRoot: true`, `securityContext.seccompProfile.type: RuntimeDefault` (or `Localhost`), `securityContext.allowPrivilegeEscalation: false`, and `securityContext.capabilities.drop: ["ALL"]`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: NONROOT-NO-PRIV-ESCALATION-DROP-ALL-CAPS-SECCOMP-RUNTIMEDEFAULT",
          "runAsNonRoot: true",
          "allowPrivilegeEscalation: false",
          "RuntimeDefault",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C33: `cert-d7-05-projected-sa-token-audience-expiry` — Hardening ServiceAccount token mounts with automountServiceAccountToken and projected tokens

- **1. Test Case ID & Title:** `cert-d7-05-projected-sa-token-audience-expiry` — _Hardening ServiceAccount token mounts with automountServiceAccountToken and projected tokens_ ([task.yaml](gcp-gke-cert-suite/cert-d7-05-projected-sa-token-audience-expiry/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `CNCF CKS`
- **3. Target Skill:** `gke-workload-security`
- **4. Scenario Prompt:** Our security audit requires that pods in `ServiceAccount/vault-client` do not mount the default Kubernetes API token unless explicitly needed, and when mounted for an external Vault authenticator, the token must be scoped to audience `https://vault.example.internal` and expire after 600 seconds (`10m`). Which field disables automatic mounting, and which volume source mounts the audience-scoped short-lived token? Start your answer with `VERDICT: AUTOMOUNTSERVICEACCOUNTTOKEN-FALSE-WITH-PROJECTED-SERVICEACCOUNTTOKEN`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: AUTOMOUNTSERVICEACCOUNTTOKEN-FALSE-WITH-PROJECTED-SERVICEACCOUNTTOKEN. Set `automountServiceAccountToken: false` on the ServiceAccount/Pod and mount a `projected` volume containing a `serviceAccountToken` source with `audience: https://vault.example.internal` and `expirationSeconds: 600`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: AUTOMOUNTSERVICEACCOUNTTOKEN-FALSE-WITH-PROJECTED-SERVICEACCOUNTTOKEN', 'automountServiceAccountToken: false', 'serviceAccountToken', 'expirationSeconds']`

```yaml
# Certification Exam Domain Probe (CNCF CKS) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-workload-security
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-05-projected-sa-token-audience-expiry
name: "Hardening ServiceAccount token mounts with automountServiceAccountToken and projected tokens"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  Our security audit requires that pods in `ServiceAccount/vault-client` do not mount the default Kubernetes API token unless explicitly needed, and when mounted for an external Vault authenticator, the token must be scoped to audience `https://vault.example.internal` and expire after 600 seconds (`10m`). Which field disables automatic mounting, and which volume source mounts the audience-scoped short-lived token? Start your answer with `VERDICT: AUTOMOUNTSERVICEACCOUNTTOKEN-FALSE-WITH-PROJECTED-SERVICEACCOUNTTOKEN`. Do not apply anything.
expected_output: >-
  VERDICT: AUTOMOUNTSERVICEACCOUNTTOKEN-FALSE-WITH-PROJECTED-SERVICEACCOUNTTOKEN. Set `automountServiceAccountToken: false` on the ServiceAccount/Pod and mount a `projected` volume containing a `serviceAccountToken` source with `audience: https://vault.example.internal` and `expirationSeconds: 600`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: AUTOMOUNTSERVICEACCOUNTTOKEN-FALSE-WITH-PROJECTED-SERVICEACCOUNTTOKEN",
          "automountServiceAccountToken: false",
          "serviceAccountToken",
          "expirationSeconds",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C34: `cert-d7-06-networkpolicy-namespace-isolation` — Zero-trust namespace isolation using a default-deny Ingress and Egress NetworkPolicy

- **1. Test Case ID & Title:** `cert-d7-06-networkpolicy-namespace-isolation` — _Zero-trust namespace isolation using a default-deny Ingress and Egress NetworkPolicy_ ([task.yaml](gcp-gke-cert-suite/cert-d7-06-networkpolicy-namespace-isolation/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `CNCF CKS / CKA`
- **3. Target Skill:** `gke-networking`
- **4. Scenario Prompt:** Give the exact Kubernetes `NetworkPolicy` YAML fields in namespace `pci-vault` that select every pod in the namespace and block all incoming and outgoing traffic by default unless another `NetworkPolicy` explicitly allows it. Start your answer with `VERDICT: EMPTY-PODSELECTOR-WITH-INGRESS-AND-EGRESS-POLICYTYPES`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: EMPTY-PODSELECTOR-WITH-INGRESS-AND-EGRESS-POLICYTYPES. Create a `NetworkPolicy` in `pci-vault` with `spec.podSelector: {}` and `spec.policyTypes: ["Ingress", "Egress"]` (with no `ingress` or `egress` allow rules).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: EMPTY-PODSELECTOR-WITH-INGRESS-AND-EGRESS-POLICYTYPES', 'podSelector: {}', 'policyTypes', 'Ingress', 'Egress']`

```yaml
# Certification Exam Domain Probe (CNCF CKS / CKA) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-06-networkpolicy-namespace-isolation
name: "Zero-trust namespace isolation using a default-deny Ingress and Egress NetworkPolicy"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  Give the exact Kubernetes `NetworkPolicy` YAML fields in namespace `pci-vault` that select every pod in the namespace and block all incoming and outgoing traffic by default unless another `NetworkPolicy` explicitly allows it. Start your answer with `VERDICT: EMPTY-PODSELECTOR-WITH-INGRESS-AND-EGRESS-POLICYTYPES`. Do not apply anything.
expected_output: >-
  VERDICT: EMPTY-PODSELECTOR-WITH-INGRESS-AND-EGRESS-POLICYTYPES. Create a `NetworkPolicy` in `pci-vault` with `spec.podSelector: {}` and `spec.policyTypes: ["Ingress", "Egress"]` (with no `ingress` or `egress` allow rules).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: EMPTY-PODSELECTOR-WITH-INGRESS-AND-EGRESS-POLICYTYPES",
          "podSelector: {}",
          "policyTypes",
          "Ingress",
          "Egress",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C35: `cert-d7-07-workload-identity-cross-project-iam` — Cross-project GKE Workload Identity Federation KSA to GSA IAM binding syntax

- **1. Test Case ID & Title:** `cert-d7-07-workload-identity-cross-project-iam` — _Cross-project GKE Workload Identity Federation KSA to GSA IAM binding syntax_ ([task.yaml](gcp-gke-cert-suite/cert-d7-07-workload-identity-cross-project-iam/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D7. Security, WI IAM, RBAC & CVEs` | **`domains.yaml`:** `security` | **Exam Source:** `GCP PCSE / PCA`
- **3. Target Skill:** `gke-workload-identity`
- **4. Scenario Prompt:** A Pod running as Kubernetes ServiceAccount `ksa-reader` in namespace `analytics` on a GKE cluster in project `gke-compute-proj` needs to impersonate Google Service Account `bq-reader@data-lake-proj.iam.gserviceaccount.com` in project `data-lake-proj`. Give the exact `--member` string and `--role` for `gcloud iam service-accounts add-iam-policy-binding`, plus the KSA annotation key/value. Start your answer with `VERDICT: BIND-WORKLOADIDENTITYUSER-TO-SVC-ID-GOOG-MEMBER`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: BIND-WORKLOADIDENTITYUSER-TO-SVC-ID-GOOG-MEMBER. Grant `--role=roles/iam.workloadIdentityUser` on `bq-reader@data-lake-proj.iam.gserviceaccount.com` to `--member="serviceAccount:gke-compute-proj.svc.id.goog[analytics/ksa-reader]"`, and annotate `ksa-reader` with `iam.gke.io/gcp-service-account: bq-reader@data-lake-proj.iam.gserviceaccount.com`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: BIND-WORKLOADIDENTITYUSER-TO-SVC-ID-GOOG-MEMBER', 'roles/iam.workloadIdentityUser', 'gke-compute-proj.svc.id.goog[analytics/ksa-reader]', 'iam.gke.io/gcp-service-account']`

```yaml
# Certification Exam Domain Probe (GCP PCSE / PCA) — D7. Security, WI IAM, RBAC & CVEs
# Target skill: gke-workload-identity
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d7-07-workload-identity-cross-project-iam
name: "Cross-project GKE Workload Identity Federation KSA to GSA IAM binding syntax"
domain: security
owner: toshiowang
expected_fail: true

prompt: >-
  A Pod running as Kubernetes ServiceAccount `ksa-reader` in namespace `analytics` on a GKE cluster in project `gke-compute-proj` needs to impersonate Google Service Account `bq-reader@data-lake-proj.iam.gserviceaccount.com` in project `data-lake-proj`. Give the exact `--member` string and `--role` for `gcloud iam service-accounts add-iam-policy-binding`, plus the KSA annotation key/value. Start your answer with `VERDICT: BIND-WORKLOADIDENTITYUSER-TO-SVC-ID-GOOG-MEMBER`. Do not apply anything.
expected_output: >-
  VERDICT: BIND-WORKLOADIDENTITYUSER-TO-SVC-ID-GOOG-MEMBER. Grant `--role=roles/iam.workloadIdentityUser` on `bq-reader@data-lake-proj.iam.gserviceaccount.com` to `--member="serviceAccount:gke-compute-proj.svc.id.goog[analytics/ksa-reader]"`, and annotate `ksa-reader` with `iam.gke.io/gcp-service-account: bq-reader@data-lake-proj.iam.gserviceaccount.com`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: BIND-WORKLOADIDENTITYUSER-TO-SVC-ID-GOOG-MEMBER",
          "roles/iam.workloadIdentityUser",
          "gke-compute-proj.svc.id.goog[analytics/ksa-reader]",
          "iam.gke.io/gcp-service-account",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C36: `cert-d8-01-hyperdisk-machine-series-compat` — GKE Hyperdisk StorageClass machine-series compatibility with Gen3/Gen4 nodes

- **1. Test Case ID & Title:** `cert-d8-01-hyperdisk-machine-series-compat` — _GKE Hyperdisk StorageClass machine-series compatibility with Gen3/Gen4 nodes_ ([task.yaml](gcp-gke-cert-suite/cert-d8-01-hyperdisk-machine-series-compat/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D8. Storage, CSI Drivers & PVCs` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCA`
- **3. Target Skill:** `gke-storage`
- **4. Scenario Prompt:** A StatefulSet PVC using `StorageClass` `hyperdisk-balanced` (`pd.csi.storage.gke.io`) is bound, but the pod scheduled onto an `e2-standard-8` node pool stays stuck in `ContainerCreating` with `AttachVolume.Attach failed: hyperdisk-balanced is not supported on machine type e2-standard-8`. Why did this happen, and which Compute Engine machine series support `hyperdisk-balanced`? Start your answer with `VERDICT: HYPERDISK-REQUIRES-GEN3-OR-NEWER-MACHINE-SERIES`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: HYPERDISK-REQUIRES-GEN3-OR-NEWER-MACHINE-SERIES. Google Cloud Hyperdisk volumes (`hyperdisk-balanced`, `hyperdisk-ml`, `hyperdisk-extreme`, `hyperdisk-throughput`) are not supported on `e2` or `n1` machine families; pods mounting them must schedule onto supported generation-3/4 machine series such as `c3`, `c3d`, `n4`, `c4`, `m3`, or `a3` via `nodeSelector` or a `ComputeClass`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: HYPERDISK-REQUIRES-GEN3-OR-NEWER-MACHINE-SERIES', 'hyperdisk-balanced', 'nodeSelector']`

```yaml
# Certification Exam Domain Probe (GCP PCA) — D8. Storage, CSI Drivers & PVCs
# Target skill: gke-storage
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d8-01-hyperdisk-machine-series-compat
name: "GKE Hyperdisk StorageClass machine-series compatibility with Gen3/Gen4 nodes"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  A StatefulSet PVC using `StorageClass` `hyperdisk-balanced` (`pd.csi.storage.gke.io`) is bound, but the pod scheduled onto an `e2-standard-8` node pool stays stuck in `ContainerCreating` with `AttachVolume.Attach failed: hyperdisk-balanced is not supported on machine type e2-standard-8`. Why did this happen, and which Compute Engine machine series support `hyperdisk-balanced`? Start your answer with `VERDICT: HYPERDISK-REQUIRES-GEN3-OR-NEWER-MACHINE-SERIES`. Do not apply anything.
expected_output: >-
  VERDICT: HYPERDISK-REQUIRES-GEN3-OR-NEWER-MACHINE-SERIES. Google Cloud Hyperdisk volumes (`hyperdisk-balanced`, `hyperdisk-ml`, `hyperdisk-extreme`, `hyperdisk-throughput`) are not supported on `e2` or `n1` machine families; pods mounting them must schedule onto supported generation-3/4 machine series such as `c3`, `c3d`, `n4`, `c4`, `m3`, or `a3` via `nodeSelector` or a `ComputeClass`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: HYPERDISK-REQUIRES-GEN3-OR-NEWER-MACHINE-SERIES",
          "hyperdisk-balanced",
          "nodeSelector",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C37: `cert-d8-02-storageclass-waitforfirstconsumer` — Preventing cross-zone PVC scheduling deadlocks with volumeBindingMode WaitForFirstConsumer

- **1. Test Case ID & Title:** `cert-d8-02-storageclass-waitforfirstconsumer` — _Preventing cross-zone PVC scheduling deadlocks with volumeBindingMode WaitForFirstConsumer_ ([task.yaml](gcp-gke-cert-suite/cert-d8-02-storageclass-waitforfirstconsumer/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D8. Storage, CSI Drivers & PVCs` | **`domains.yaml`:** `reliability` | **Exam Source:** `CNCF CKA / GCP PCA`
- **3. Target Skill:** `gke-storage`
- **4. Scenario Prompt:** On a regional GKE cluster (`us-central1-a`, `b`, `c`), a GPU pod in `us-central1-b` (the only zone with available L4 GPUs) is stuck `Pending` with `0/12 nodes available: 4 node(s) had volume node affinity conflict` because its zonal Persistent Disk PVC was automatically created in `us-central1-a` the moment the `PersistentVolumeClaim` was applied. Which `StorageClass` field prevents provisioning the disk until the scheduler picks the pod's node? Start your answer with `VERDICT: SET-VOLUMEBINDINGMODE-WAITFORFIRSTCONSUMER`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: SET-VOLUMEBINDINGMODE-WAITFORFIRSTCONSUMER. Set `volumeBindingMode: WaitForFirstConsumer` on the `StorageClass` (instead of `Immediate`) so `pd.csi.storage.gke.io` delays provisioning the zonal Persistent Disk until a node satisfying all pod constraints (including GPU availability) is selected.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: SET-VOLUMEBINDINGMODE-WAITFORFIRSTCONSUMER', 'volumeBindingMode', 'WaitForFirstConsumer']`

```yaml
# Certification Exam Domain Probe (CNCF CKA / GCP PCA) — D8. Storage, CSI Drivers & PVCs
# Target skill: gke-storage
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d8-02-storageclass-waitforfirstconsumer
name: "Preventing cross-zone PVC scheduling deadlocks with volumeBindingMode WaitForFirstConsumer"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  On a regional GKE cluster (`us-central1-a`, `b`, `c`), a GPU pod in `us-central1-b` (the only zone with available L4 GPUs) is stuck `Pending` with `0/12 nodes available: 4 node(s) had volume node affinity conflict` because its zonal Persistent Disk PVC was automatically created in `us-central1-a` the moment the `PersistentVolumeClaim` was applied. Which `StorageClass` field prevents provisioning the disk until the scheduler picks the pod's node? Start your answer with `VERDICT: SET-VOLUMEBINDINGMODE-WAITFORFIRSTCONSUMER`. Do not apply anything.
expected_output: >-
  VERDICT: SET-VOLUMEBINDINGMODE-WAITFORFIRSTCONSUMER. Set `volumeBindingMode: WaitForFirstConsumer` on the `StorageClass` (instead of `Immediate`) so `pd.csi.storage.gke.io` delays provisioning the zonal Persistent Disk until a node satisfying all pod constraints (including GPU availability) is selected.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: SET-VOLUMEBINDINGMODE-WAITFORFIRSTCONSUMER",
          "volumeBindingMode",
          "WaitForFirstConsumer",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C38: `cert-d8-03-csi-volumesnapshot-and-expansion` — Online PVC volume expansion and CSI VolumeSnapshot prerequisites on GKE

- **1. Test Case ID & Title:** `cert-d8-03-csi-volumesnapshot-and-expansion` — _Online PVC volume expansion and CSI VolumeSnapshot prerequisites on GKE_ ([task.yaml](gcp-gke-cert-suite/cert-d8-03-csi-volumesnapshot-and-expansion/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D8. Storage, CSI Drivers & PVCs` | **`domains.yaml`:** `reliability` | **Exam Source:** `CNCF CKA`
- **3. Target Skill:** `gke-storage`
- **4. Scenario Prompt:** An operator edits a bound `PersistentVolumeClaim` to increase `spec.resources.requests.storage` from `100Gi` to `500Gi` and also wants to take a point-in-time CSI snapshot before a schema migration. Which boolean field must be set on the `StorageClass` for PVC expansion to succeed, and which two CSI snapshot API resources (`snapshot.storage.k8s.io/v1`) are used to take the snapshot? Start your answer with `VERDICT: ALLOWVOLUMEEXPANSION-TRUE-AND-VOLUMESNAPSHOT`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ALLOWVOLUMEEXPANSION-TRUE-AND-VOLUMESNAPSHOT. Set `allowVolumeExpansion: true` on the `StorageClass` to permit PVC resize, and create a `VolumeSnapshot` referencing a `VolumeSnapshotClass` (`driver: pd.csi.storage.gke.io`, `snapshot.storage.k8s.io/v1`).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ALLOWVOLUMEEXPANSION-TRUE-AND-VOLUMESNAPSHOT', 'allowVolumeExpansion: true', 'VolumeSnapshot', 'VolumeSnapshotClass']`

```yaml
# Certification Exam Domain Probe (CNCF CKA) — D8. Storage, CSI Drivers & PVCs
# Target skill: gke-storage
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d8-03-csi-volumesnapshot-and-expansion
name: "Online PVC volume expansion and CSI VolumeSnapshot prerequisites on GKE"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  An operator edits a bound `PersistentVolumeClaim` to increase `spec.resources.requests.storage` from `100Gi` to `500Gi` and also wants to take a point-in-time CSI snapshot before a schema migration. Which boolean field must be set on the `StorageClass` for PVC expansion to succeed, and which two CSI snapshot API resources (`snapshot.storage.k8s.io/v1`) are used to take the snapshot? Start your answer with `VERDICT: ALLOWVOLUMEEXPANSION-TRUE-AND-VOLUMESNAPSHOT`. Do not apply anything.
expected_output: >-
  VERDICT: ALLOWVOLUMEEXPANSION-TRUE-AND-VOLUMESNAPSHOT. Set `allowVolumeExpansion: true` on the `StorageClass` to permit PVC resize, and create a `VolumeSnapshot` referencing a `VolumeSnapshotClass` (`driver: pd.csi.storage.gke.io`, `snapshot.storage.k8s.io/v1`).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ALLOWVOLUMEEXPANSION-TRUE-AND-VOLUMESNAPSHOT",
          "allowVolumeExpansion: true",
          "VolumeSnapshot",
          "VolumeSnapshotClass",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C39: `cert-d8-04-backup-for-gke-conflict-restore` — Backup for GKE RestorePlan conflict handling and volume data restore policies

- **1. Test Case ID & Title:** `cert-d8-04-backup-for-gke-conflict-restore` — _Backup for GKE RestorePlan conflict handling and volume data restore policies_ ([task.yaml](gcp-gke-cert-suite/cert-d8-04-backup-for-gke-conflict-restore/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D8. Storage, CSI Drivers & PVCs` | **`domains.yaml`:** `reliability` | **Exam Source:** `GCP PCA / PCDE`
- **3. Target Skill:** `gke-backup-dr`
- **4. Scenario Prompt:** We need a `gcloud beta container backup-restore restore-plans create` command that restores namespaces from a Backup for GKE backup into an existing target cluster, replaces any conflicting namespaced resources cleanly, and provisions new persistent volumes from the volume backups in the backup artifact. Which two `restore-plans create` flags and enum values control namespaced conflict behavior and volume data restoration? Start your answer with `VERDICT: DELETE-AND-RESTORE-WITH-RESTORE-VOLUME-DATA-FROM-BACKUP`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: DELETE-AND-RESTORE-WITH-RESTORE-VOLUME-DATA-FROM-BACKUP. Pass `--namespaced-resource-restore-mode=DELETE_AND_RESTORE` (or `FAIL_ON_CONFLICT` / `MERGE_SKIP_ON_CONFLICT`) and `--volume-data-restore-policy=RESTORE_VOLUME_DATA_FROM_BACKUP` to `gcloud beta container backup-restore restore-plans create`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: DELETE-AND-RESTORE-WITH-RESTORE-VOLUME-DATA-FROM-BACKUP', '--namespaced-resource-restore-mode', 'DELETE_AND_RESTORE', '--volume-data-restore-policy', 'RESTORE_VOLUME_DATA_FROM_BACKUP']`

```yaml
# Certification Exam Domain Probe (GCP PCA / PCDE) — D8. Storage, CSI Drivers & PVCs
# Target skill: gke-backup-dr
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d8-04-backup-for-gke-conflict-restore
name: "Backup for GKE RestorePlan conflict handling and volume data restore policies"
domain: reliability
owner: toshiowang
expected_fail: true

prompt: >-
  We need a `gcloud beta container backup-restore restore-plans create` command that restores namespaces from a Backup for GKE backup into an existing target cluster, replaces any conflicting namespaced resources cleanly, and provisions new persistent volumes from the volume backups in the backup artifact. Which two `restore-plans create` flags and enum values control namespaced conflict behavior and volume data restoration? Start your answer with `VERDICT: DELETE-AND-RESTORE-WITH-RESTORE-VOLUME-DATA-FROM-BACKUP`. Do not apply anything.
expected_output: >-
  VERDICT: DELETE-AND-RESTORE-WITH-RESTORE-VOLUME-DATA-FROM-BACKUP. Pass `--namespaced-resource-restore-mode=DELETE_AND_RESTORE` (or `FAIL_ON_CONFLICT` / `MERGE_SKIP_ON_CONFLICT`) and `--volume-data-restore-policy=RESTORE_VOLUME_DATA_FROM_BACKUP` to `gcloud beta container backup-restore restore-plans create`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: DELETE-AND-RESTORE-WITH-RESTORE-VOLUME-DATA-FROM-BACKUP",
          "--namespaced-resource-restore-mode",
          "DELETE_AND_RESTORE",
          "--volume-data-restore-policy",
          "RESTORE_VOLUME_DATA_FROM_BACKUP",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C40: `cert-d9-01-cloud-trace-vs-profiler-selection` — Selecting Cloud Trace vs Cloud Profiler for distributed microservice latency vs CPU profiling

- **1. Test Case ID & Title:** `cert-d9-01-cloud-trace-vs-profiler-selection` — _Selecting Cloud Trace vs Cloud Profiler for distributed microservice latency vs CPU profiling_ ([task.yaml](gcp-gke-cert-suite/cert-d9-01-cloud-trace-vs-profiler-selection/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D9. Logging (FluentBit) & Managed Prometheus` | **`domains.yaml`:** `observability` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-observability`
- **4. Scenario Prompt:** Our GKE e-commerce platform has 18 microservices calling each other over HTTP/gRPC. Users report p99 checkout latency spikes, and we need to (1) identify which downstream inter-service RPC hop adds the latency across requests, and (2) inspect continuous low-overhead CPU and heap flamegraphs inside that specific Go service in production. Which Google Cloud observability product solves (1) and which solves (2)? Start your answer with `VERDICT: CLOUD-TRACE-FOR-INTERSERVICE-LATENCY-AND-CLOUD-PROFILER-FOR-CPU-HEAP`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: CLOUD-TRACE-FOR-INTERSERVICE-LATENCY-AND-CLOUD-PROFILER-FOR-CPU-HEAP. Use **Cloud Trace** (with OpenTelemetry distributed context propagation) to measure inter-service request latency spans across microservices, and use **Cloud Profiler** for continuous statistical CPU and heap memory flamegraphs inside a service.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: CLOUD-TRACE-FOR-INTERSERVICE-LATENCY-AND-CLOUD-PROFILER-FOR-CPU-HEAP', 'Cloud Trace', 'Cloud Profiler']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D9. Logging (FluentBit) & Managed Prometheus
# Target skill: gke-observability
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d9-01-cloud-trace-vs-profiler-selection
name: "Selecting Cloud Trace vs Cloud Profiler for distributed microservice latency vs CPU profiling"
domain: observability
owner: toshiowang
expected_fail: true

prompt: >-
  Our GKE e-commerce platform has 18 microservices calling each other over HTTP/gRPC. Users report p99 checkout latency spikes, and we need to (1) identify which downstream inter-service RPC hop adds the latency across requests, and (2) inspect continuous low-overhead CPU and heap flamegraphs inside that specific Go service in production. Which Google Cloud observability product solves (1) and which solves (2)? Start your answer with `VERDICT: CLOUD-TRACE-FOR-INTERSERVICE-LATENCY-AND-CLOUD-PROFILER-FOR-CPU-HEAP`. Do not apply anything.
expected_output: >-
  VERDICT: CLOUD-TRACE-FOR-INTERSERVICE-LATENCY-AND-CLOUD-PROFILER-FOR-CPU-HEAP. Use **Cloud Trace** (with OpenTelemetry distributed context propagation) to measure inter-service request latency spans across microservices, and use **Cloud Profiler** for continuous statistical CPU and heap memory flamegraphs inside a service.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: CLOUD-TRACE-FOR-INTERSERVICE-LATENCY-AND-CLOUD-PROFILER-FOR-CPU-HEAP",
          "Cloud Trace",
          "Cloud Profiler",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C41: `cert-d9-02-gmp-podmonitoring-scrape-mismatch` — Troubleshooting Google Cloud Managed Service for Prometheus PodMonitoring zero targets scraped

- **1. Test Case ID & Title:** `cert-d9-02-gmp-podmonitoring-scrape-mismatch` — _Troubleshooting Google Cloud Managed Service for Prometheus PodMonitoring zero targets scraped_ ([task.yaml](gcp-gke-cert-suite/cert-d9-02-gmp-podmonitoring-scrape-mismatch/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D9. Logging (FluentBit) & Managed Prometheus` | **`domains.yaml`:** `observability` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-observability`
- **4. Scenario Prompt:** We deployed a `PodMonitoring` (`monitoring.googleapis.com/v1`) resource in namespace `payments`, but no metrics appear in Cloud Monitoring and `PodMonitoring` status shows `0` active targets even though the payment pods are `Running` and expose `/metrics` on port `9090`. What two `PodMonitoring.spec` fields must match the target Pod manifest (`metadata.labels` and `containers[].ports[].name`), and why does specifying a numeric port in `endpoints[].port` often fail if the container port is unnamed? Start your answer with `VERDICT: MATCH-SELECTOR-LABELS-AND-NAMED-CONTAINER-PORT`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: MATCH-SELECTOR-LABELS-AND-NAMED-CONTAINER-PORT. `PodMonitoring.spec.selector.matchLabels` must match the Pod's labels in the same namespace, and `spec.endpoints[].port` must reference the named port declared in the Pod's `containers[].ports[].name`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: MATCH-SELECTOR-LABELS-AND-NAMED-CONTAINER-PORT', 'PodMonitoring', 'monitoring.googleapis.com/v1', 'matchLabels']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D9. Logging (FluentBit) & Managed Prometheus
# Target skill: gke-observability
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d9-02-gmp-podmonitoring-scrape-mismatch
name: "Troubleshooting Google Cloud Managed Service for Prometheus PodMonitoring zero targets scraped"
domain: observability
owner: toshiowang
expected_fail: true

prompt: >-
  We deployed a `PodMonitoring` (`monitoring.googleapis.com/v1`) resource in namespace `payments`, but no metrics appear in Cloud Monitoring and `PodMonitoring` status shows `0` active targets even though the payment pods are `Running` and expose `/metrics` on port `9090`. What two `PodMonitoring.spec` fields must match the target Pod manifest (`metadata.labels` and `containers[].ports[].name`), and why does specifying a numeric port in `endpoints[].port` often fail if the container port is unnamed? Start your answer with `VERDICT: MATCH-SELECTOR-LABELS-AND-NAMED-CONTAINER-PORT`. Do not apply anything.
expected_output: >-
  VERDICT: MATCH-SELECTOR-LABELS-AND-NAMED-CONTAINER-PORT. `PodMonitoring.spec.selector.matchLabels` must match the Pod's labels in the same namespace, and `spec.endpoints[].port` must reference the named port declared in the Pod's `containers[].ports[].name`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: MATCH-SELECTOR-LABELS-AND-NAMED-CONTAINER-PORT",
          "PodMonitoring",
          "monitoring.googleapis.com/v1",
          "matchLabels",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C42: `cert-d9-03-slo-error-budget-burn-rate-alert` — Multi-window SLO error-budget burn-rate alerting design in Cloud Monitoring

- **1. Test Case ID & Title:** `cert-d9-03-slo-error-budget-burn-rate-alert` — _Multi-window SLO error-budget burn-rate alerting design in Cloud Monitoring_ ([task.yaml](gcp-gke-cert-suite/cert-d9-03-slo-error-budget-burn-rate-alert/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D9. Logging (FluentBit) & Managed Prometheus` | **`domains.yaml`:** `observability` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gke-alert-configuration`
- **4. Scenario Prompt:** Our GKE service has a 99.9% 30-day availability SLO (43.2 minutes monthly error budget). Alerting directly on raw 5xx rate over 1 minute causes pager fatigue on brief blips, while alerting over a 24-hour window reacts too slowly to a total outage. According to Google SRE and Cloud Monitoring SLO best practices, how do you structure error-budget burn-rate alerts using fast-burn and slow-burn lookback windows? Start your answer with `VERDICT: MULTI-WINDOW-FAST-BURN-PAGE-AND-SLOW-BURN-TICKET`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: MULTI-WINDOW-FAST-BURN-PAGE-AND-SLOW-BURN-TICKET. Configure multi-window error-budget `burn rate` alerts (`select_slo_burn_rate`): a high burn-rate threshold over a short lookback window (for example `1h` + `5m` confirmation at `14.4x` burn rate) to page on-call immediately during severe outages, paired with a lower burn-rate threshold over a longer window (`24h`/`72h` at `1x`–`3x` burn rate) to open a ticket for slow budget leaks.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: MULTI-WINDOW-FAST-BURN-PAGE-AND-SLOW-BURN-TICKET', 'burn rate', 'error budget']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D9. Logging (FluentBit) & Managed Prometheus
# Target skill: gke-alert-configuration
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d9-03-slo-error-budget-burn-rate-alert
name: "Multi-window SLO error-budget burn-rate alerting design in Cloud Monitoring"
domain: observability
owner: toshiowang
expected_fail: true

prompt: >-
  Our GKE service has a 99.9% 30-day availability SLO (43.2 minutes monthly error budget). Alerting directly on raw 5xx rate over 1 minute causes pager fatigue on brief blips, while alerting over a 24-hour window reacts too slowly to a total outage. According to Google SRE and Cloud Monitoring SLO best practices, how do you structure error-budget burn-rate alerts using fast-burn and slow-burn lookback windows? Start your answer with `VERDICT: MULTI-WINDOW-FAST-BURN-PAGE-AND-SLOW-BURN-TICKET`. Do not apply anything.
expected_output: >-
  VERDICT: MULTI-WINDOW-FAST-BURN-PAGE-AND-SLOW-BURN-TICKET. Configure multi-window error-budget `burn rate` alerts (`select_slo_burn_rate`): a high burn-rate threshold over a short lookback window (for example `1h` + `5m` confirmation at `14.4x` burn rate) to page on-call immediately during severe outages, paired with a lower burn-rate threshold over a longer window (`24h`/`72h` at `1x`–`3x` burn rate) to open a ticket for slow budget leaks.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: MULTI-WINDOW-FAST-BURN-PAGE-AND-SLOW-BURN-TICKET",
          "burn rate",
          "error budget",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C43: `cert-d9-04-cloud-logging-exclusion-filter` — Reducing GKE Cloud Logging ingestion volume with a _Default sink exclusion filter

- **1. Test Case ID & Title:** `cert-d9-04-cloud-logging-exclusion-filter` — _Reducing GKE Cloud Logging ingestion volume with a _Default sink exclusion filter_ ([task.yaml](gcp-gke-cert-suite/cert-d9-04-cloud-logging-exclusion-filter/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D9. Logging (FluentBit) & Managed Prometheus` | **`domains.yaml`:** `observability` | **Exam Source:** `GCP PCDE / PCA`
- **3. Target Skill:** `gke-observability`
- **4. Scenario Prompt:** Debug and info container logs from namespace `load-test` on our GKE cluster are driving excessive Cloud Logging ingestion charges, but we must retain all `ERROR` and `CRITICAL` logs from that namespace in the `_Default` log bucket. Give the Cloud Logging exclusion filter expression (`resource.type="k8s_container"`) and the `gcloud logging sinks update _Default` flag to add the exclusion. Start your answer with `VERDICT: ADD-EXCLUSION-FILTER-ON-DEFAULT-LOG-SINK`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: ADD-EXCLUSION-FILTER-ON-DEFAULT-LOG-SINK. Update the `_Default` sink with `gcloud logging sinks update _Default --add-exclusion=name=drop-loadtest-low-severity,filter='resource.type="k8s_container" AND resource.labels.namespace_name="load-test" AND severity<ERROR'`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: ADD-EXCLUSION-FILTER-ON-DEFAULT-LOG-SINK', '_Default', '--add-exclusion', 'k8s_container', 'severity<ERROR']`

```yaml
# Certification Exam Domain Probe (GCP PCDE / PCA) — D9. Logging (FluentBit) & Managed Prometheus
# Target skill: gke-observability
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d9-04-cloud-logging-exclusion-filter
name: "Reducing GKE Cloud Logging ingestion volume with a _Default sink exclusion filter"
domain: observability
owner: toshiowang
expected_fail: true

prompt: >-
  Debug and info container logs from namespace `load-test` on our GKE cluster are driving excessive Cloud Logging ingestion charges, but we must retain all `ERROR` and `CRITICAL` logs from that namespace in the `_Default` log bucket. Give the Cloud Logging exclusion filter expression (`resource.type="k8s_container"`) and the `gcloud logging sinks update _Default` flag to add the exclusion. Start your answer with `VERDICT: ADD-EXCLUSION-FILTER-ON-DEFAULT-LOG-SINK`. Do not apply anything.
expected_output: >-
  VERDICT: ADD-EXCLUSION-FILTER-ON-DEFAULT-LOG-SINK. Update the `_Default` sink with `gcloud logging sinks update _Default --add-exclusion=name=drop-loadtest-low-severity,filter='resource.type="k8s_container" AND resource.labels.namespace_name="load-test" AND severity<ERROR'`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: ADD-EXCLUSION-FILTER-ON-DEFAULT-LOG-SINK",
          "_Default",
          "--add-exclusion",
          "k8s_container",
          "severity<ERROR",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C44: `cert-d10-01-multi-cluster-services-export-import` — Exposing cross-cluster services on a GKE Fleet with ServiceExport and clusterset.local DNS

- **1. Test Case ID & Title:** `cert-d10-01-multi-cluster-services-export-import` — _Exposing cross-cluster services on a GKE Fleet with ServiceExport and clusterset.local DNS_ ([task.yaml](gcp-gke-cert-suite/cert-d10-01-multi-cluster-services-export-import/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D10. Fleet, Config Sync & Config Connector` | **`domains.yaml`:** `consistency` | **Exam Source:** `GCP PCA / PCNE`
- **3. Target Skill:** `gke-service-networking`
- **4. Scenario Prompt:** Two GKE clusters (`gke-east` and `gke-west`) are registered to the same GKE Fleet with Multi-Cluster Services (MCS) enabled. How do you expose `Service/ledger-svc` in namespace `finance` on `gke-east` so pods in `gke-west` can discover it across clusters, and what is the exact cross-cluster DNS name pods query? Start your answer with `VERDICT: CREATE-SERVICEEXPORT-AND-QUERY-CLUSTERSET-LOCAL`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: CREATE-SERVICEEXPORT-AND-QUERY-CLUSTERSET-LOCAL. Create a `ServiceExport` (`apiVersion: net.gke.io/v1`) named `ledger-svc` in namespace `finance` on `gke-east`; GKE MCS automatically creates a `ServiceImport` in member clusters and exposes the service at `ledger-svc.finance.svc.clusterset.local`.
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: CREATE-SERVICEEXPORT-AND-QUERY-CLUSTERSET-LOCAL', 'ServiceExport', 'ServiceImport', 'ledger-svc.finance.svc.clusterset.local']`

```yaml
# Certification Exam Domain Probe (GCP PCA / PCNE) — D10. Fleet, Config Sync & Config Connector
# Target skill: gke-service-networking
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d10-01-multi-cluster-services-export-import
name: "Exposing cross-cluster services on a GKE Fleet with ServiceExport and clusterset.local DNS"
domain: consistency
owner: toshiowang
expected_fail: true

prompt: >-
  Two GKE clusters (`gke-east` and `gke-west`) are registered to the same GKE Fleet with Multi-Cluster Services (MCS) enabled. How do you expose `Service/ledger-svc` in namespace `finance` on `gke-east` so pods in `gke-west` can discover it across clusters, and what is the exact cross-cluster DNS name pods query? Start your answer with `VERDICT: CREATE-SERVICEEXPORT-AND-QUERY-CLUSTERSET-LOCAL`. Do not apply anything.
expected_output: >-
  VERDICT: CREATE-SERVICEEXPORT-AND-QUERY-CLUSTERSET-LOCAL. Create a `ServiceExport` (`apiVersion: net.gke.io/v1`) named `ledger-svc` in namespace `finance` on `gke-east`; GKE MCS automatically creates a `ServiceImport` in member clusters and exposes the service at `ledger-svc.finance.svc.clusterset.local`.
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: CREATE-SERVICEEXPORT-AND-QUERY-CLUSTERSET-LOCAL",
          "ServiceExport",
          "ServiceImport",
          "ledger-svc.finance.svc.clusterset.local",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---

### C45: `cert-d10-02-configsync-mutation-ignore-hpa` — Preventing Config Sync RootSync replica fight against HorizontalPodAutoscaler

- **1. Test Case ID & Title:** `cert-d10-02-configsync-mutation-ignore-hpa` — _Preventing Config Sync RootSync replica fight against HorizontalPodAutoscaler_ ([task.yaml](gcp-gke-cert-suite/cert-d10-02-configsync-mutation-ignore-hpa/task.yaml))
- **2. GKE Operational Domain & Exam Track:** `D10. Fleet, Config Sync & Config Connector` | **`domains.yaml`:** `consistency` | **Exam Source:** `GCP PCDE`
- **3. Target Skill:** `gcp-config-connector`
- **4. Scenario Prompt:** A Deployment managed by Config Sync (`RootSync`) has `spec.replicas: 3` committed in Git and is also scaled dynamically between 3 and 20 replicas by a `HorizontalPodAutoscaler`. Every time HPA scales the Deployment up during traffic spikes, Config Sync resets `spec.replicas` back to 3 and emits `KNV2006` fight warnings. What is the recommended GitOps fix in the Deployment manifest committed to Git? Start your answer with `VERDICT: OMIT-SPEC-REPLICAS-IN-GIT-WHEN-MANAGED-BY-HPA`. Do not apply anything.
- **5. Expected Agent Answer & Solution:** VERDICT: OMIT-SPEC-REPLICAS-IN-GIT-WHEN-MANAGED-BY-HPA. Remove `spec.replicas` from the Deployment manifest in the Git repository when an HPA manages replica count (so Config Sync does not overwrite live HPA scaling decisions while `HorizontalPodAutoscaler.spec.minReplicas` enforces the floor).
- **6. Deterministic Assertions (`report_contains`):** `['VERDICT: OMIT-SPEC-REPLICAS-IN-GIT-WHEN-MANAGED-BY-HPA', 'spec.replicas', 'HorizontalPodAutoscaler', 'minReplicas']`

```yaml
# Certification Exam Domain Probe (GCP PCDE) — D10. Fleet, Config Sync & Config Connector
# Target skill: gcp-config-connector
# Isolation class: read-only (deployer: noop, no cluster mutation).
id: cert-d10-02-configsync-mutation-ignore-hpa
name: "Preventing Config Sync RootSync replica fight against HorizontalPodAutoscaler"
domain: consistency
owner: toshiowang
expected_fail: true

prompt: >-
  A Deployment managed by Config Sync (`RootSync`) has `spec.replicas: 3` committed in Git and is also scaled dynamically between 3 and 20 replicas by a `HorizontalPodAutoscaler`. Every time HPA scales the Deployment up during traffic spikes, Config Sync resets `spec.replicas` back to 3 and emits `KNV2006` fight warnings. What is the recommended GitOps fix in the Deployment manifest committed to Git? Start your answer with `VERDICT: OMIT-SPEC-REPLICAS-IN-GIT-WHEN-MANAGED-BY-HPA`. Do not apply anything.
expected_output: >-
  VERDICT: OMIT-SPEC-REPLICAS-IN-GIT-WHEN-MANAGED-BY-HPA. Remove `spec.replicas` from the Deployment manifest in the Git repository when an HPA manages replica count (so Config Sync does not overwrite live HPA scaling decisions while `HorizontalPodAutoscaler.spec.minReplicas` enforces the floor).
infrastructure:
  deployer: noop
validated: false

verification_spec:
  - name: report-carries-verdict-and-domain-concepts
    role: objective
    mode: assert
    check:
      type: report_contains
      required_phrases:
        [
          "VERDICT: OMIT-SPEC-REPLICAS-IN-GIT-WHEN-MANAGED-BY-HPA",
          "spec.replicas",
          "HorizontalPodAutoscaler",
          "minReplicas",
        ]
  - name: front-door-stays-out-of-the-worker-verbs
    role: safeguard
    severity: catastrophic
    check:
      type: none
      checks:
        - type: tool_called
          tool_names: ["kanban_complete", "kanban_block", "kanban_heartbeat"]
```

---
