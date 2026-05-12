# Scion Implementation of `docs/demo.md`

This document maps the [original demo proposal](demo.md) (Google Chat-based, two-agent) onto the Scion-based implementation (multi-agent platform team, CLI / web dashboard / Inbox Tray as the human surface). The original `docs/demo.md` is preserved as the source-of-truth narrative — this doc describes what changes when you run it on Scion.

## What changes from the original

| Aspect | Original (`demo.md`) | Scion implementation |
|---|---|---|
| **Substrate** | OpenClaw + Google Chat | Scion (Hub + Broker + web dashboard, all running locally) |
| **Agent count** | 2 (Cluster_Operator, Dev_Team_Agent) | 3+ (`platform-coordinator` + `upgrade-coordinator` + `dev-workload-guardian`, with `node-pool-provisioner` and `workload-deployer` available for fan-out) |
| **Inter-agent UX** | @-mentions in a shared Chat space | `scion message` from coordinator to specialists; coordinator narrates the back-and-forth |
| **Human UX** | Chat thread | `scion attach` to coordinator (terminal) + Scion web dashboard's Inbox Tray |
| **GKE actions** | "the agents do it" (unspecified plumbing) | Real calls via the [GKE remote MCP server](https://docs.cloud.google.com/kubernetes-engine/docs/reference/mcp) and the local [`gke-mcp` binary](https://github.com/GoogleCloudPlatform/gke-mcp) |
| **Persistent constraints** | "stored in `MEMORY.md`" | Same — `/workspace/MEMORY.md`, single-writer = `platform-coordinator` |
| **Persona names** | `Cluster_Operator`, `Dev_Team_Agent` | Templates are `upgrade-coordinator` and `dev-workload-guardian`; coordinator narrates them with the original persona names so the demo's narrative reads the same |

## What stays the same

- The narrative beats: a mandatory upgrade, a Readiness Score, a resilience-gap mitigation, a no-change-zone constraint set by the human, a negotiated execution window, and a captured decision in `MEMORY.md`.
- The patterns demonstrated: semantic negotiation (Readiness Scores, not raw YAML), JIT scaling, persistent context via `MEMORY.md`, cross-agent synergy.
- The personas' character: calm/analytical for `Cluster_Operator`; performance-driven/protective for `Dev_Team_Agent`.

## Scenario 1: Collaborative Upgrade Handshake — Scion mapping

Phase-by-phase, what runs in the Scion implementation:

### Phase 1 — Initial Deployment & Intent

The original demo opens with `Dev_Team_Agent` reporting a successful deployment and a single-replica resilience setup.

**Scion implementation:** the seed `MEMORY.md` (rendered by `bootstrap.sh` from `workspace-seed/MEMORY.md`) records the in-scope workload as single-replica. The `platform-coordinator` reads this on its first turn and grounds the rest of the conversation in it. No actual deployment happens during the demo; either point at an existing single-replica workload or apply a stub (see `demos/upgrade-handshake/README.md`).

### Phase 2 — Infrastructure Signal

The original has `Cluster_Operator` initiating with a mandatory-upgrade ping.

**Scion implementation:** the *human* initiates by giving the `platform-coordinator` the opening prompt (rendered from `opening-prompt.md.template` with the `GKE_TARGET_VERSION` filled in). The coordinator then spawns `upgrade-coordinator` (announcing it as `Cluster_Operator`) and briefs it with the upgrade target. This is a small inversion from the original — the upgrade trigger is human-driven, not autonomous — and matches reality better since GKE upgrades are usually scheduled events known to the team in advance.

### Phase 3 — Risk Assessment & Progressive Disclosure

The original has `Dev_Team_Agent` producing a Readiness Score (42/100, "Low") and surfacing the resilience gap to the human.

**Scion implementation:** in parallel with spawning `upgrade-coordinator`, the coordinator spawns `dev-workload-guardian` (announcing it as `Dev_Team_Agent`) and asks for a Readiness Score for the in-scope workloads. The guardian uses local `gke-mcp` (`query_logs` for recent error/restart history) and the cluster state to score; it returns a structured score + reasoning + recommended mitigations. The coordinator narrates this to the human in `Dev_Team_Agent` voice.

### Phase 4 — Human-in-the-Loop Negotiation

The original has the human providing high-level intent: "make it resilient, but not during business hours."

**Scion implementation:** the coordinator surfaces the guardian's recommendation (e.g., "scale to 3 replicas") and the upgrade-coordinator's plan as a single negotiation message via `sciontool status ask_user`. The human responds in the attached terminal (or the web dashboard's Inbox Tray). The coordinator captures the no-change-zone constraint and writes it into `/workspace/MEMORY.md` for future requests.

### Phase 5 — Handshake & Exclusion Window

The original has the agents agreeing on a final plan with pre-flight scaling, an upgrade window, and an exclusion zone.

**Scion implementation:** the coordinator spawns `workload-deployer` for the pre-flight scale-to-3 (since that's a workload-side change, not a node-pool change), and re-engages `upgrade-coordinator` with the agreed window. Both specialists `ask_user` again at their actual write boundaries (`apply_k8s_manifest`, `update_cluster`); the coordinator surfaces those for confirmation. Once the human approves at the boundaries, execution proceeds.

`upgrade-coordinator` monitors the rollout via `get_k8s_rollout_status`, `get_operation`, and `query_logs`, and pauses on anomalies (the original's "auto-pause if error rates exceed 1%").

### Decision capture

Throughout, the coordinator updates `/workspace/MEMORY.md` with: the agreed window, the no-change zone, the chosen surge/max-unavailable settings, and any incidents. Future requests against this cluster start with that context.

## Scenario 2: N2 vs N4 Performance Benchmark — Scion mapping (deferred)

The Scion templates needed for Scenario 2 (`cost-optimizer`, `workload-deployer`, `node-pool-provisioner`) are already in the library. A second demo project under `demos/n2-vs-n4-benchmark/` will compose them when phase 2 starts. Sketch:

- `platform-coordinator` receives the user's "compare N2 vs N4 for service-alpha" intent
- Spawns `cost-optimizer` to model the comparison and propose
- On approval, spawns `node-pool-provisioner` to create the parallel pool, then `workload-deployer` to fan `service-alpha` across both
- `dev-workload-guardian` produces Readiness Scores throughout
- Coordinator narrates the benchmark results and captures the decision in `MEMORY.md`

## Why this isn't a verbatim port

Two architectural changes from the original demo are intentional:

1. **Narrowed agent scope** — the original `Cluster_Operator` is too broad to run autonomously (multi-cluster balancing, upgrades, scans, certs, log rotation, all in one). Scion splits this into focused specialists each with one verb and one MCP-endpoint scope. The demo only needs `upgrade-coordinator`; future use cases compose other specialists.
2. **Coordinator-mediated handshakes** — Scion's convention is that worker agents do not message each other directly; an orchestrator routes between them. The original's @-mentioned chat thread is reproduced by the coordinator narrating both sides of the handshake, which scales to N specialists where peer-to-peer would not.
