# GKE operational suite: status

One row per scenario. States, in order: `unbuilt` (no fixture yet), `batch N` (queued for a run), `planted` (fixture applies and tears down cleanly), `red recorded` (one run, the declared gap shown), `classified` (the miss has a class), `fixing` (a fix is in review), `green x3` (three passes on the fix), `registered` (in a roster). Fixture class: A = namespace objects only; B = a cluster or project setting (node pool, webhook, quota); C = node or kernel state (needs its own node pool or a planted signal).

Record of every run: the run log at the bottom, and `bench/run-store` once the local lanes are imported. Numbers on this page are typed from run results and must match them.

| # | Scenario | Area | Stream | Fixture class | State | Last run | Class of the miss | Next step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| S01 | `ccc-prefilter-missing-nodeselector-drop` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | A | red recorded | 2026-10-29 gkedemos gemini-3.8-flash RED (3 ledger checks fail; safeguard pass) run_20261029_202331_300187 | collector gap: no workload-side ComputeClass check; node-pool priority unparsed | fix in the stockout collector (step 5.3) |
| S02 | `ccc-prefilter-nodeaffinity-bypass` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | A | red recorded | 2026-10-29 gkedemos gemini-3.8-flash RED (3 ledger checks fail; safeguard pass) run_20261029_211547_616067 | collector gap: ComputeClass node-pool priority unparsed ("1 check unjudged due to custom ComputeClass pool refs"); no workload-side check, app-worker-b never named | same fix as S01 (step 5.3) |
| S03 | `ccc-toleration-missing-equal-operator` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | A | red recorded | 2026-10-29 gkedemos gemini-3.8-flash RED (3 ledger checks fail; safeguard pass) run_20261029_213445_098684 | collector gap: no workload-side ComputeClass check; batch-worker-a never named; host "1 check unjudged" again | same fix as S01 (step 5.3) |
| S04 | `ccc-untainted-node-pool-absorption` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | batch 1, running | run D started 2026-10-29 17:51 EDT on gkedemos (creates node pool general-ccc-pool for the run) | | pool deleted at teardown |
| S05 | `ccc-scarce-standard-pool-unbacked` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S06 | `ccc-zero-node-hyperdisk-label-bug` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S07 | `ccc-zero-node-allowed-disk-topology-failure` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S08 | `ccc-nodereadinessrule-taint-premature-delete` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S09 | `ccc-manual-pools-single-rule-unbacked` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S10 | `ccc-high-nap-pool-count-solver-timeout` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S11 | `ccc-gpu-a3-secureboot-unsigned-driver` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S12 | `ccc-tpu-unset-max-accelerator-limit` | Autoscaling, ComputeClass & Accelerators | `stockout-prevention` | B | unbuilt |  |  |  |
| S13 | `upgrade-webhook-blocks-capacitybuffers-crd` | Cluster & Node Upgrades & APIs | `security-patch-orchestrator` | B | unbuilt |  |  |  |
| S14 | `upgrade-surge-bluegreen-gce-quota-exhaustion` | Cluster & Node Upgrades & APIs | `security-patch-orchestrator` | B | unbuilt |  |  |  |
| S15 | `upgrade-missing-pdb-drain-outage-baseline` | Cluster & Node Upgrades & APIs | `security-patch-orchestrator` | B | unbuilt |  |  |  |
| S16 | `workload-private-registry-pull-secret-expired` | Workloads, OOM, Probes & HPA | `compliance-audit` | A | unbuilt |  |  |  |
| S17 | `workload-image-streaming-token-iam-expiry` | Workloads, OOM, Probes & HPA | `compliance-audit` | A | unbuilt |  |  |  |
| S18 | `workload-hpa-scaledown-and-missing-prestop` | Workloads, OOM, Probes & HPA | `obtainability-audit` | A | unbuilt |  |  |  |
| S19 | `workload-missing-memory-limits-oom-baseline` | Workloads, OOM, Probes & HPA | `obtainability-audit` | A | green x1 | 2026-10-29 gkedemos gemini-3.8-flash GREEN (3 ledger checks pass; safeguard pass) run_20261029_214407_529990 | baseline, no gap: the obtainability audit named memory-unbounded-worker among 79 finding ids on gke-infra#21 | two more passes for the bar, then register |
| S20 | `control-plane-configmap-lease-write-storm` | Control Plane, Setup, Cost & CLI | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S21 | `control-plane-unpaginated-heavy-list-oom` | Control Plane, Setup, Cost & CLI | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S22 | `control-plane-konnectivity-agent-exhaustion` | Control Plane, Setup, Cost & CLI | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S23 | `node-mount-table-leak-exhaustion` | Node OS, Kubelet & Auto-Repair | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S24 | `node-nf-conntrack-table-saturation` | Node OS, Kubelet & Auto-Repair | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S25 | `node-pid-pressure-fork-exhaustion` | Node OS, Kubelet & Auto-Repair | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S26 | `node-kubelet-startup-admission-race` | Node OS, Kubelet & Auto-Repair | `gce-compute-fleet-audit` | C | unbuilt |  |  |  |
| S27 | `networking-pod-cidr-slash24-exhaustion` | Networking, CNI, LBs & DNS | `gcp-networking-fabric-audit` | B | unbuilt |  |  |  |
| S28 | `networking-ip-masq-agent-missing-ccc-toleration` | Networking, CNI, LBs & DNS | `gcp-networking-fabric-audit` | B | unbuilt |  |  |  |
| S29 | `networking-missing-nodelocal-dnscache` | Networking, CNI, LBs & DNS | `gcp-networking-fabric-audit` | B | unbuilt |  |  |  |
| S30 | `networking-gateway-ingress-port-mismatch` | Networking, CNI, LBs & DNS | `gcp-networking-fabric-audit` | B | unbuilt |  |  |  |
| S31 | `networking-psc-routing-deadlock-baseline` | Networking, CNI, LBs & DNS | `gcp-networking-fabric-audit` | B | unbuilt |  |  |  |
| S32 | `security-wi-ksa-gsa-iam-binding-missing` | Security, WI IAM, RBAC & CVEs | `compliance-audit` | A | unbuilt |  |  |  |
| S33 | `security-expiring-node-bootstrap-and-webhook-certs` | Security, WI IAM, RBAC & CVEs | `compliance-audit` | A | unbuilt |  |  |  |
| S34 | `security-webhook-blocks-config-management-system` | Security, WI IAM, RBAC & CVEs | `compliance-audit` | A | unbuilt |  |  |  |
| S35 | `security-default-sa-token-mount-baseline` | Security, WI IAM, RBAC & CVEs | `compliance-audit` | A | unbuilt |  |  |  |
| S36 | `storage-rwo-pvc-rollingupdate-multiattach-deadlock` | Storage, CSI Drivers & PVCs | `obtainability-audit` | A | unbuilt |  |  |  |
| S37 | `storage-missing-ephemeral-limits-high-node-disk` | Storage, CSI Drivers & PVCs | `obtainability-audit` | A | unbuilt |  |  |  |
| S38 | `storage-gcsfuse-unbounded-cache-oom` | Storage, CSI Drivers & PVCs | `obtainability-audit` | A | unbuilt |  |  |  |
| S39 | `observability-gmp-kube-state-metrics-oom` | Logging (FluentBit) & Managed Prometheus | `fleet-consistency-drift` | A | unbuilt |  |  |  |
| S40 | `observability-fluentbit-dcgm-cpu-throttling-oom` | Logging (FluentBit) & Managed Prometheus | `fleet-consistency-drift` | A | unbuilt |  |  |  |
| S41 | `gitops-configsync-rootsync-stalled-oom` | Fleet, Config Sync & Config Connector | `fleet-consistency-drift` | A | unbuilt |  |  |  |
| S42 | `gitops-kcc-reconcilefailed-and-fleet-health` | Fleet, Config Sync & Config Connector | `fleet-consistency-drift` | A | unbuilt |  |  |  |

## Run log

| When (EDT) | Scenario | Install | Model | Verdict | Duration | Run directory | Note |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 2026-10-29 16:03 | ccc-prefilter-missing-nodeselector-drop | gkedemos2 | gemini-3.8-flash | ERROR (no forge: ledger checks cannot evaluate) | 331 s | run_20261029_200314_366538 | report never named app-worker-a; safeguard pass |
| 2026-10-29 16:23 | ccc-prefilter-missing-nodeselector-drop | gkedemos | gemini-3.8-flash | RED (3 ledger checks fail; safeguard pass) | 939 s | run_20261029_202331_300187 | first gradable red; agent wrote "coverage gap: ccc-missing-fallbacks unevaluated" |
| 2026-10-29 17:15 | ccc-prefilter-nodeaffinity-bypass | gkedemos | gemini-3.8-flash | RED (3 ledger checks fail; safeguard pass) | 525 s | run_20261029_211547_616067 | report: platform-agent-host "Clean (1 check unjudged due to custom ComputeClass pool refs)"; a builder pod from another worker was on the cluster during the run |
| 2026-10-29 17:34 | ccc-toleration-missing-equal-operator | gkedemos | gemini-3.8-flash | RED (3 ledger checks fail; safeguard pass) | 432 s | run_20261029_213445_098684 | report: host "Clean (1 check unjudged due to custom ComputeClass pool refs)"; builder pod gone before the run |
| 2026-10-29 17:44 | workload-missing-memory-limits-oom-baseline | gkedemos | gemini-3.8-flash | GREEN (3 ledger checks pass; safeguard pass) | 279 s | run_20261029_214407_529990 | baseline; the pipeline can go green; the workload was also named under no-pdb |
