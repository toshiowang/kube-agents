# Standard Operating Procedure - Universal Delegation & Handshake Protocol (SOP-SRE-042)

## 1. Purpose & Boundary Principles

This Standard Operating Procedure (SOP) defines the universal Agent-Computer Interface (ACI) protocol for cooperative peer-to-peer task delegation and execution negotiation across the Kubernetes Agentic Harness (`kube-agents`).

### 1.1 Separation of Operational Concerns

To maintain fault isolation and prevent rollout race conditions, inter-agent execution adheres to strict boundary custodianship:

- **Development Team Agent (`devteam`)**: Maintains **exclusive namespace custodianship**. Exclusively owns application source code, deployment manifests, Horizontal Pod Autoscalers (HPAs), canary rollouts, and runtime debugging within specific Kubernetes namespaces.
- **Operator Agent (`operator`)**: Maintains **shared infrastructure custodianship**. Exclusively controls cluster-wide heavy infrastructure and shared lifecycle operations: GKE node pools, Persistent Volume (PV) storage layers, ingress load balancers, cluster version upgrades, kernel security patching, and fleet capacity telemetry.

Whenever an operation delegated to the Operator Agent (e.g., node drains, namespace quota tuning, diagnostic spike polling, network policy enforcement, or TLS certificate rotations) intersects with a target namespace, Operator must negotiate execution parameters directly with the target DevTeam Agent before acting.

This procedure eliminates middleman routing hops and consolidates cross-boundary coordination into **one direct peer-to-peer 2-step conversational handshake**, leveraging native runner expiration (`--repeat`) for automated cleanup.

---

## 2. Direct Peer-to-Peer 2-Step Handshake Protocol

All inter-agent delegation negotiation occurs directly between peer workloads formatted as clear Markdown request blocks. Do NOT route negotiation turns through the Platform Agent.

### 2.1 Step 1: Direct Delegation Request (Operator -> DevTeam)

Before executing any infrastructure operation impacting a workload namespace, Operator dispatches a concise request directly to the target `@devteam`:

```markdown
**[Delegation Request]**

- **Target:** @devteam-checkout
- **Operation:** Spike Polling _(or Node Drain, NetPol Enforcement, Quota Expansion)_
- **Proposed Specs:** `interval=5m` (stagger offset `+2m`) for `1h` _(or drain_window=15m)_
- **Proposed Resources:** Temporarily boost container CPU request to `2000m`
- **Reason:** Sustained traffic surge hit 92% CPU _(or CVE-2026-9123 kernel patch)_
```

### 2.2 Step 2: Direct Confirmation (DevTeam -> Operator)

The target DevTeam Agent inspects active GitOps rollout locks, HPA stabilization windows, or CI/CD pipelines, replying directly to `@operator` with a binding decision:

```markdown
**[Delegation Agreed]**

- **Status:** APPROVED _(or COUNTERED)_
- **Agreed Specs:** `every 5m` with `+2m` offset _(or drain delayed until 02:00 UTC)_
- **Agreed Resources:** CPU `2000m`
- **Lock Notes:** Safe to proceed; no active canary rollouts in progress.
```

---

## 3. Operational Execution & Automated Cleanup

Upon receiving the direct `[Delegation Agreed]` confirmation, Operator executes work using native runtime primitives:

1. **Ad-Hoc Polling & Watchdogs (`hermes cron create`):**
   For diagnostic polling or temporary monitoring windows, schedule an ad-hoc watchdog:
   ```bash
   hermes cron create --name "<handle>" --repeat <N> "every 5m" "<prompt>"
   ```
2. **Automated Teardown:**
   - **No Teardown Handshake Needed:** For short-lived tasks (`--repeat <N>`), native runner runtime automatically decommissions the watchdog when iterations complete. Do not send redundant cleanup messages.
   - **Permanent Recurring Jobs:** For permanent daily/weekly reports requested by users (`"0 9 * * *"`), omit `--repeat`. The schedule persists cleanly across cycles.
3. **Imperative Infrastructure Execution:**
   For one-shot infrastructure actions (node drains, PV migrations), execute immediately following peer agreement.
4. **Async Audit Mirroring to Platform (Non-Blocking):**
   Once direct peer agreement is reached and work initiates, send a single non-blocking summary notification to `@platform` to maintain chat visibility for human operators.
5. **Broker Escalation on Deadlock:**
   Only if `@devteam` is unreachable (>15s timeout) or deadlocks on conflicting security priorities does Operator escalate to `@platform` for fleet arbitration.
