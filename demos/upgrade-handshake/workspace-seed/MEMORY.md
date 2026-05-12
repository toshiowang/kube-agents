# Platform Team — Shared MEMORY

> **Single writer**: only `platform-coordinator` writes to this file.
> Specialists may read it for context; updates flow through the coordinator.

## Demo: Collaborative Upgrade Handshake

This MEMORY.md seeds the upgrade-handshake demo: a workload-aware GKE upgrade negotiation between the upgrade specialist, the workload safety reviewer, and the human.

## In-scope cluster

- **Project:**     ${GKE_PROJECT}
- **Location:**    ${GKE_LOCATION}
- **Cluster:**     ${GKE_CLUSTER}

## In-scope namespaces

${GKE_NAMESPACES_IN_SCOPE}

## In-scope workloads

| Namespace | Workload | Owner | Notes |
|---|---|---|---|
| ${PROD_NAMESPACE} | ${PRIMARY_WORKLOAD} | (developer) | Single replica at session start to mimic the demo's resilience-gap setup. The demo expects the team to detect this and propose scaling before any upgrade. |

## No-change zones

(none seeded — the human will set these during the negotiation, e.g. "no infra changes during business hours today, marketing push")

## Decision log

(empty — the coordinator will append entries here as decisions are made)

## Notes for the coordinator

- This is a sandbox cluster. Treat it as if it were production for the demo's purposes (HITL gates on every write), but real-world consequence is bounded.
- Scenario-specific structured data (Readiness Score, upgrade window, recommended replicas) lives in this file under the relevant section once produced.
