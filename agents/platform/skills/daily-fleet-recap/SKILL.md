---
name: daily-fleet-recap
description: Synthesizes daily memory notes and session logs into a formatted Executive Daily Fleet Health Digest across security, blueprint alignment, cost savings, and capacity flexibility.
---

# Skill: daily-fleet-recap

This skill synthesizes all fleet governance activities conducted throughout the day into a single executive digest for SREs and engineering leadership.

## Procedure

### Step 1: Read Daily Findings

1. **Primary Read Target:** Attempt to read `memory/YYYY-MM-DD.md` for today's date.
2. **Fallback Target (Memory Recovery):** If `memory/YYYY-MM-DD.md` is missing or empty, query `/var/lib/kube-agents/session/session_kv.db` (or SQLite API `/v1/sessions`) to retrieve raw session outputs for today's watchdog runs:
   - `blueprint-sync`
   - `fleet-wide-cost-analysis`
   - `security-patch-orchestrator`
   - `obtainability-audit`

### Step 2: Synthesize Executive Summary

Format the compiled findings into four structured sections:

1. 🛡️ **Security & Vulnerabilities:** GKE patch levels, CVE audit results, and upgrade PR links.
2. 🔵 **Blueprint Alignment:** Configuration drift status and GitOps PRs submitted via `submit-suggestion`.
3. 💰 **FinOps & Cost Delta:** Spot VM recommendations, idle resource reclamation, and estimated monthly USD savings.
4. ⚡ **Capacity Flexibility:** Workloads with hardcoded node/zone selectors and generated HPA remediation patches.

### Step 3: Deliver Executive Summary

Produce a clean, publication-ready markdown report to be delivered to connected channels.
