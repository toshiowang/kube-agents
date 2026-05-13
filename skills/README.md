# Shared GKE Skills

Canonical, vendored copies of GKE skills used by every agent composition in this repo (OpenClaw and Scion). Sourced from `GoogleCloudPlatform/gke-mcp/skills/` — see `SKILLS_VERSION` for the pinned upstream commit.

## Who consumes these

- **OpenClaw agents** (`openclaw/agents/{operator,devteam}/skills/`) — each entry is a relative symlink into this directory. The OpenClaw install script dereferences symlinks when copying agent assets to the workspace.
- **Scion role templates** (`templates/<role>/skills/`) — each entry is a relative symlink into this directory. Scion auto-copies skills into the harness path at agent start and resolves symlinks naturally.

## Refreshing from upstream

1. Bump `SKILLS_VERSION` to the new gke-mcp commit SHA.
2. For each skill directory present here, replace its contents with the matching upstream `gke-mcp/skills/<name>/`.
3. If new skills are needed, copy the directory in and update the consumer template/agent's `skills/` to add a symlink.
4. If a skill is no longer needed, remove its directory and any consumer symlinks pointing at it.

This is intentionally manual for phase 1 — automate when the cadence justifies a script.

## Inventory

| Skill | Used by |
|---|---|
| gke-app-onboarding | OpenClaw devteam; Scion workload-deployer |
| gke-backup-dr | OpenClaw operator |
| gke-cluster-creator | Scion node-pool-provisioner |
| gke-cluster-lifecycle | OpenClaw operator; Scion upgrade-coordinator |
| gke-compute-class-creator | Scion cost-optimizer |
| gke-cost-analysis | OpenClaw operator; Scion cost-optimizer |
| gke-cost-optimization | Scion cost-optimizer |
| gke-inference-quickstart | OpenClaw devteam |
| gke-networking-edge | OpenClaw operator |
| gke-observability | OpenClaw operator; Scion dev-workload-guardian |
| gke-productionize | OpenClaw operator, devteam; Scion workload-deployer |
| gke-reliability | OpenClaw operator, devteam; Scion upgrade-coordinator, dev-workload-guardian |
| gke-workload-scaling | OpenClaw operator, devteam; Scion node-pool-provisioner, workload-deployer |
| gke-workload-security | OpenClaw operator, devteam; Scion dev-workload-guardian |
