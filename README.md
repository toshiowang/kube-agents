# kube-agents: The Kubernetes Agentic Harness

The k8s agentic harness will fundamentally redefine the DevOps presentation layer by replacing traditional interfaces like kubectl, gcloud, and the Pantheon console with intelligent, autonomous agents. By replacing the static, imperative nature of the traditional Kubernetes presentation layer with an autonomous agentic harness, we transition from reactive manual management to proactive, intent-driven operations.

## Key Components

### 1. Kubernetes Operator Agent (`operator`)
An autonomous custodian of the infrastructure configured with a calm, analytical persona (`SOUL.md`). It manages global concerns like multi-cluster balancing, capacity, upgrades, and platform security policies, while executing scheduled cron jobs (health patrols, CVE scans, log rotations, certificate scans).

### 2. Development Team Agent (`devteam`)
A production-safety coach and application workload custodian configured with a performance-driven persona (`SOUL.md`). It represents developer interests, enforcing schema validation, resource requests/limits templates, and automated NetworkPolicies, while running development-specific cron tasks (rollout watches, error rate monitors, and SLO checks).

---

## Installation & Setup

Choose how you want to deploy the Kubernetes agentic capabilities.

### Run on Scion (preferred, in development)

The active direction for kube-agents is a **GKE Platform Team** of focused, narrow-blast-radius role agents (cluster upgrade, workload safety, node-pool provisioning, cost optimization, workload deployment) coordinated by a `platform-coordinator`, hosted on [Scion](https://github.com/GoogleCloudPlatform/scion). The first runnable scenario lives at:

- **[demos/upgrade-handshake/](demos/upgrade-handshake/README.md)** — Scenario 1 (Collaborative Upgrade Handshake) end-to-end on local Scion against a real GKE cluster, using both the local `gke-mcp` binary and the remote `container.googleapis.com/mcp` server (with a token-refreshing proxy).

Reusable building blocks live at:

- **[templates/](templates/README.md)** — pure role templates (the library)
- **[skills/](skills/README.md)** — shared GKE skills, vendored from `GoogleCloudPlatform/gke-mcp`
- **[tools/](tools/README.md)** — host-side MCP infrastructure scripts

### Use in OpenClaw (legacy)

The earlier prototype is still installable into [OpenClaw](https://openclaw.ai/) via a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/gke-labs/kube-agents/main/openclaw/scripts/install.sh | bash
```

For more details, see the [OpenClaw Integration Guide](openclaw/README.md).

### Showcasing in Action
To test the OpenClaw harness's dynamic routing, automated remediation, and cross-agent negotiations, follow the step-by-step [Showcase & Demo Scenarios guide](openclaw/README.md#showcasing-the-harness-in-action-demo-scenarios).

#### Installing from a Custom Branch or Fork

If you want to install from a forked repository or a custom branch (for example, to test changes), you should export `REPO` and `BRANCH` environment variables before running the install script. This ensures both `curl` and the installer use the correct sources:

```bash
export REPO="https://github.com/<owner>/kube-agents"
export BRANCH="<branch-name>"
curl -fsSL "${REPO}/raw/${BRANCH}/openclaw/scripts/install.sh" | bash
```

This will fetch the script from your branch and configure the installer to download assets from the same fork and branch.

## Disclaimer

This is not an officially supported Google product.

This project is not eligible for the Google Open Source Software Vulnerability Rewards Program.
