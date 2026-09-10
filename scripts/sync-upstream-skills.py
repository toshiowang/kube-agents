#!/usr/bin/env python3
"""Syncs GKE agent skills from the upstream google/skills repository (skills/cloud)."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

UPSTREAM_REPO = "https://github.com/google/skills.git"
UPSTREAM_SKILLS_PATH = os.path.join("skills", "cloud")
SKILL_PREFIX = "gke-"

# The lock records what the last sync produced: the upstream commit it read and a digest of
# every mirrored file after substitutions and footers. scripts/test_sync_upstream_skills.py
# checks the tree against it on every pull request, so a direct edit to a mirrored file fails
# there instead of vanishing at the next sync. A deliberate deviation is listed under
# `local_overrides` with the pull request that made it; the sync wipes those and says so.
LOCK_FILE = os.path.join("scripts", "upstream_skills_lock.json")
LOCK_INDENT = 2
DIGEST_ALGORITHM = "sha256"
LOCK_REPO_KEY = "upstream_repo"
LOCK_PATH_KEY = "upstream_path"
LOCK_COMMIT_KEY = "upstream_commit"
LOCK_FILES_KEY = "files"
LOCK_OVERRIDES_KEY = "local_overrides"
# A full object name: an abbreviated one is refused by a depth-1 fetch, and a branch or tag name
# would sync a moving ref while recording whichever commit it happened to resolve to.
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
GIT_HEAD = "HEAD"
GIT_FETCH_HEAD = "FETCH_HEAD"
# Editor and OS droppings (.DS_Store, swap files) are not part of the mirror.
HIDDEN_FILE_PREFIX = "."

# Target agents where upstream GKE skills should be synced.
#
# Upstream skills from google/skills (skills/cloud) target the Platform Agent (agents/platform/).
# Cluster Agent skills (agents/cluster/skills/) are not synced from upstream: they are repo-native
# templates tailored specifically for single-cluster runtime debugging and operations (see AGENTS.md),
# with cluster-specific personas and diagnostic tooling that an upstream overwrite would wipe.
# Consequently, DEFAULT_TARGET_AGENTS is ["platform"] and cluster skills are maintained independently
# in this repository.
DEFAULT_TARGET_AGENTS = ["platform"]
SKILL_AGENT_OVERRIDES = {
    # Per-skill target agent overrides if specific skills should go to additional/alternative agents.
}

SKILL_MD_FILENAME = "SKILL.md"
UTF_8_ENCODING = "utf-8"
SUBSTITUTION_COUNT = 1

GKE_WORKLOAD_SECURITY_OLD_NETPOL_SNIPPET = """**Enable Network Policy Enforcement:**

```bash
gcloud container clusters update <cluster-name> \\
    --update-addons=NetworkPolicy=ENABLED \\
    --region <region>
```

> [!NOTE] If your cluster uses Dataplane V2 (`--enable-dataplane-v2`), Network
> Policy enforcement is built-in and this step is not required (and may fail)."""

GKE_WORKLOAD_SECURITY_NEW_NETPOL_SNIPPET = """**Check Network Policy Enforcement & Dataplane:**

Before modifying cluster networking, inspect whether NetworkPolicy enforcement
is already active or provided natively by Dataplane V2:

```bash
gcloud container clusters describe <cluster-name> \\
    --location <location> \\
    --format='value(networkConfig.datapathProvider,networkPolicy.enabled)'
```

- If `datapathProvider` is `ADVANCED_DATAPATH` (Dataplane V2), NetworkPolicy
  enforcement is built-in natively via eBPF/Cilium from cluster creation. Calico
  addons cannot be enabled and are not needed.
- If `networkPolicy.enabled` is `True`, Calico enforcement is already enabled on nodes.
- If neither is active, enable Calico network policy enforcement using the two-step
  sequence below.

**Enable Network Policy Enforcement (non-DPv2 clusters):**

Enabling network policy enforcement on clusters without Dataplane V2 requires
two sequential commands in this order: first enable the Calico addon on the
control plane, then enable network policy enforcement on the nodes. GKE rejects
`--enable-network-policy` with HTTP 400 until the addon is enabled, and `gcloud`
rejects both flags in a single invocation.

```bash
# Step 1: Enable the NetworkPolicy addon on the control plane
gcloud container clusters update <cluster-name> \\
    --update-addons=NetworkPolicy=ENABLED \\
    --region <region>

# Step 2: Enable NetworkPolicy enforcement on the nodes (node pools may be recreated; this can take several minutes)
gcloud container clusters update <cluster-name> \\
    --enable-network-policy \\
    --region <region>
```"""

# In-place content substitutions applied to freshly-synced skills to correct upstream defects
# where an appended footer is insufficient (e.g. multi-step remediation commands). An entry is
# `(old, new)` for the skill's SKILL.md, or `(relative_path, old, new)` for any other file in the
# skill directory, such as a reference or an asset.
SKILL_SUBSTITUTIONS = {
    "gke-workload-security": [
        (
            GKE_WORKLOAD_SECURITY_OLD_NETPOL_SNIPPET,
            GKE_WORKLOAD_SECURITY_NEW_NETPOL_SNIPPET,
        ),
    ],
}

# Marker that identifies our auto-injected footer, so injection is idempotent and
# the footer can be recognized/stripped later if needed.
FOOTER_MARKER = "<!-- kube-agents: local addition (auto-injected by sync-upstream-skills.py) -->"

# Upstream skills are copied over verbatim on every sync (the local dir is rmtree'd first), so any
# local edits are wiped. Anything this repository needs an upstream skill to say therefore belongs
# here rather than in the skill file: these footers are the single source of truth for it and are
# re-appended after each sync. Two things need saying today — the GKE create/lifecycle skills must
# keep pointing at this repo's Cluster Agent profile lifecycle, which upstream knows nothing about
# (see agents/platform/skills/cluster-agent-lifecycle/SKILL.md for the mechanics they reference),
# and gke-networking must not present `--dns-endpoint` as unconditionally safe.
SKILL_FOOTERS = {
    "gke-cluster-creation": f"""{FOOTER_MARKER}

## Required final step: provision the Cluster Agent profile

Creating a cluster is **not complete** until it has a Cluster Agent. A managed cluster and its
Cluster Agent profile are **created together** — never leave a newly created cluster without a
profile. Immediately after `create_cluster` succeeds and the cluster is reachable, create its
dedicated **Cluster Agent** profile (this is what makes the cluster delegable for runtime
debugging). Use the [cluster-agent-lifecycle](../cluster-agent-lifecycle/SKILL.md) skill:

```bash
python3 /opt/data/scripts/cluster_agent_profile.py create \\
  --project "<project>" --cluster "<cluster>" --location "<location>"
```

The command is idempotent, so it is safe to re-run. This gives the new cluster an agent
immediately. (The `cluster-agent-reconcile` cron would also pick it up on its next run — it
manages every cluster in the project, so no labeling is required.)

## Cluster Agent Profile Teardown

A managed cluster and its Cluster Agent profile are **deleted together**. When a cluster is
decommissioned/deleted, also remove its dedicated **Cluster Agent** profile (created at onboarding).
Use the [cluster-agent-lifecycle](../cluster-agent-lifecycle/SKILL.md) skill:

```bash
python3 /opt/data/scripts/cluster_agent_profile.py delete \\
  --project "<project>" --cluster "<cluster>" --location "<location>"
```

Do not delete a Cluster Agent profile while its cluster still exists.

Deleting the profile here is the immediate, preferred path. As a backstop, the hourly
`cluster-agent-reconcile` job auto-prunes any profile whose cluster is definitively gone, so a
profile missed during teardown is cleaned up on the next reconcile cycle.
""",
    "gke-networking": f"""{FOOTER_MARKER}

## Before you pass `--dns-endpoint`

The `get-credentials --dns-endpoint` example above works only on a cluster that publishes a DNS
endpoint **and** has `controlPlaneEndpointsConfig.dnsEndpointConfig.allowExternalTraffic` set to
true. Check first:

```bash
gcloud container clusters describe {{cluster_name}} --region {{region}} \\
  --format='value(controlPlaneEndpointsConfig.dnsEndpointConfig.endpoint,controlPlaneEndpointsConfig.dnsEndpointConfig.allowExternalTraffic)'
```

Do not infer support from the command succeeding. When external traffic is disabled, a caller that
Google treats as internal gets a warning rather than an error, plus a kubeconfig pointing at the
DNS endpoint that then returns HTTP 403 on first use — a failure that surfaces one step later than
its cause. `gcloud container clusters update {{cluster_name}} --enable-dns-access` turns the
setting on.

The Platform Agent's own tooling makes this decision per cluster in
`/opt/data/scripts/gke_endpoint.py`, so `switch_kube_context` and the Cluster Agent profile
scaffolding already pass the flag exactly when it applies; the check above is for the times you
run `get-credentials` by hand. That decision is re-read about once a minute per cluster, so after
enabling the setting, wait a moment before retrying rather than concluding it did not work.
""",
}


def apply_substitutions(dest_path, skill_name):
    """Apply in-place string substitutions to a freshly-synced skill's files.

    Used when an upstream defect must be corrected in-place (such as a remediation
    sequence where an appended footer would still leave the broken command in the
    body of the skill).

    Idempotent: if replacement text is already present, the substitution is skipped.
    Returns True if at least one substitution was applied, else False.
    """
    substitutions = SKILL_SUBSTITUTIONS.get(skill_name)
    if not substitutions:
        return False

    by_file = {}
    for entry in substitutions:
        relative_path, target, replacement = entry if len(entry) == 3 else (SKILL_MD_FILENAME, *entry)
        by_file.setdefault(relative_path, []).append((target, replacement))

    modified_any = False
    for relative_path, pairs in by_file.items():
        path = os.path.join(dest_path, relative_path)
        if not os.path.isfile(path):
            print(f"Warning: {path} not found; cannot apply substitutions.", file=sys.stderr)
            continue

        with open(path, "r", encoding=UTF_8_ENCODING) as f:
            content = f.read()

        modified = False
        for target, replacement in pairs:
            if replacement in content:
                continue
            if target in content:
                content = content.replace(target, replacement, SUBSTITUTION_COUNT)
                modified = True
            else:
                print(
                    f"Warning: target snippet for substitution not found in {skill_name}/{relative_path}",
                    file=sys.stderr,
                )

        if modified:
            with open(path, "w", encoding=UTF_8_ENCODING) as f:
                f.write(content)
            modified_any = True

    return modified_any


def inject_footer(dest_path, skill_name):
    """Append this repository's footer for a skill to its freshly-synced SKILL.md.

    Idempotent: does nothing if the skill has no footer configured or the footer marker is
    already present. Returns True if a footer was written, else False.
    """
    footer = SKILL_FOOTERS.get(skill_name)
    if footer is None:
        return False

    skill_md = os.path.join(dest_path, SKILL_MD_FILENAME)
    if not os.path.isfile(skill_md):
        print(f"Warning: {skill_md} not found; cannot inject Cluster Agent footer.", file=sys.stderr)
        return False

    with open(skill_md, "r", encoding=UTF_8_ENCODING) as f:
        existing = f.read()
    if FOOTER_MARKER in existing:
        return False

    separator = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    with open(skill_md, "a", encoding=UTF_8_ENCODING) as f:
        f.write(separator + footer)
    return True


def _mirror_agents():
    return sorted(set(DEFAULT_TARGET_AGENTS + [a for agents in SKILL_AGENT_OVERRIDES.values() for a in agents]))


def agent_skills_dir(repo_root, agent):
    return os.path.join(repo_root, "agents", agent, "skills")


def mirrored_files(repo_root):
    """Repo-relative paths of every file under a mirrored (prefix-named) skill directory."""
    paths = []
    for agent in _mirror_agents():
        skills_dir = agent_skills_dir(repo_root, agent)
        if not os.path.isdir(skills_dir):
            continue
        for name in sorted(os.listdir(skills_dir)):
            skill_dir = os.path.join(skills_dir, name)
            if not name.startswith(SKILL_PREFIX) or not os.path.isdir(skill_dir):
                continue
            for dirpath, _, filenames in os.walk(skill_dir):
                for filename in filenames:
                    if filename.startswith(HIDDEN_FILE_PREFIX):
                        continue
                    paths.append(os.path.relpath(os.path.join(dirpath, filename), repo_root))
    return sorted(paths)


def file_digest(path):
    h = hashlib.new(DIGEST_ALGORITHM)
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def build_lock(repo_root, upstream_commit, local_overrides=None):
    """The lock for the tree as it stands: one digest per mirrored file."""
    return {
        LOCK_REPO_KEY: UPSTREAM_REPO,
        LOCK_PATH_KEY: UPSTREAM_SKILLS_PATH,
        LOCK_COMMIT_KEY: upstream_commit,
        LOCK_FILES_KEY: {rel: file_digest(os.path.join(repo_root, rel)) for rel in mirrored_files(repo_root)},
        LOCK_OVERRIDES_KEY: dict(sorted((local_overrides or {}).items())),
    }


def load_lock(repo_root):
    with open(os.path.join(repo_root, LOCK_FILE), "r", encoding=UTF_8_ENCODING) as f:
        return json.load(f)


def write_lock(repo_root, lock):
    with open(os.path.join(repo_root, LOCK_FILE), "w", encoding=UTF_8_ENCODING) as f:
        json.dump(lock, f, indent=LOCK_INDENT, sort_keys=True)
        f.write("\n")


def check_lock(repo_root, lock):
    """Problems between the tree and the lock; empty when every mirrored file is accounted for.

    A file counts as accounted for when its digest matches the lock or it is listed under
    local_overrides. An override whose file matches the lock anyway is stale and is reported
    too, so the list stays an honest record of what the next sync will wipe.
    """
    locked = lock.get(LOCK_FILES_KEY, {})
    overrides = lock.get(LOCK_OVERRIDES_KEY, {})
    actual = {rel: file_digest(os.path.join(repo_root, rel)) for rel in mirrored_files(repo_root)}
    problems = []
    for rel in sorted(set(actual) - set(locked)):
        problems.append(f"{rel}: not in the lock (added outside the sync)")
    for rel in sorted(set(locked) - set(actual)):
        problems.append(f"{rel}: in the lock but missing from the tree")
    for rel in sorted(set(actual) & set(locked)):
        if actual[rel] != locked[rel] and rel not in overrides:
            problems.append(f"{rel}: differs from the last sync and is not listed under {LOCK_OVERRIDES_KEY}")
    for rel in sorted(overrides):
        if rel not in actual:
            problems.append(f"{rel}: listed under {LOCK_OVERRIDES_KEY} but missing from the tree")
        elif rel in locked and actual[rel] == locked[rel]:
            problems.append(f"{rel}: listed under {LOCK_OVERRIDES_KEY} but matches the last sync (stale entry)")
    return problems


def run_cmd(cmd, cwd=None):
    """Runs a shell command and returns the result, raising an exception on failure."""
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Stdout:\n{res.stdout}", file=sys.stderr)
        print(f"Stderr:\n{res.stderr}", file=sys.stderr)
        res.check_returncode()
    return res

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    parser = argparse.ArgumentParser(description=__doc__)
    pin = parser.add_mutually_exclusive_group()
    pin.add_argument("--upstream-commit", help=f"Full 40-hex upstream commit to sync from. Default: the commit recorded in {LOCK_FILE}.")
    pin.add_argument("--latest", action="store_true", help="Sync from the upstream default branch head and record the new commit in the lock.")
    parser.add_argument("--check", action="store_true", help="Compare the tree with the lock and exit non-zero on any difference; no network.")
    args = parser.parse_args()

    lock_present = os.path.isfile(os.path.join(repo_root, LOCK_FILE))
    if args.check:
        problems = check_lock(repo_root, load_lock(repo_root))
        for problem in problems:
            print(problem, file=sys.stderr)
        sys.exit(1 if problems else 0)

    # Re-running after a SKILL_SUBSTITUTIONS or SKILL_FOOTERS edit must reproduce the pinned
    # upstream, not pull in whatever upstream has merged since; advancing is a separate decision.
    pinned_commit = args.upstream_commit
    if pinned_commit is None and not args.latest and lock_present:
        pinned_commit = load_lock(repo_root).get(LOCK_COMMIT_KEY)
    if pinned_commit is not None and not FULL_SHA_RE.match(pinned_commit):
        parser.error(f"--upstream-commit must be a full 40-hex commit, got {pinned_commit!r}")

    try:
        print("Creating temporary directory for shallow clone...")
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"Cloning upstream repository (depth 1): {UPSTREAM_REPO}...")
            run_cmd([
                "git", "clone", "--depth", "1",
                UPSTREAM_REPO, tmpdir
            ])
            if pinned_commit:
                print(f"Checking out pinned upstream commit {pinned_commit}...")
                run_cmd(["git", "fetch", "--depth", "1", "origin", pinned_commit], cwd=tmpdir)
                run_cmd(["git", "checkout", "--quiet", GIT_FETCH_HEAD], cwd=tmpdir)
            upstream_commit = run_cmd(["git", "rev-parse", GIT_HEAD], cwd=tmpdir).stdout.strip()
            previous_overrides = load_lock(repo_root).get(LOCK_OVERRIDES_KEY, {}) if lock_present else {}
            
            upstream_skills_dir = os.path.join(tmpdir, UPSTREAM_SKILLS_PATH)
            if not os.path.isdir(upstream_skills_dir):
                print(f"Error: upstream skills directory not found in clone: {upstream_skills_dir}", file=sys.stderr)
                sys.exit(1)
                
            # Discover all skills that start with the prefix (e.g. 'gke-')
            discovered_skills = sorted([
                name for name in os.listdir(upstream_skills_dir)
                if name.startswith(SKILL_PREFIX) and os.path.isdir(os.path.join(upstream_skills_dir, name))
            ])
            
            if not discovered_skills:
                print(f"Warning: No skills found matching prefix '{SKILL_PREFIX}' in {upstream_skills_dir}", file=sys.stderr)
                return
                
            print(f"\nDiscovered {len(discovered_skills)} skills matching prefix '{SKILL_PREFIX}':")
            for name in discovered_skills:
                print(f"  - {name}")

            # Prune obsolete local skill directories that were renamed/removed upstream
            for agent in _mirror_agents():
                skills_dir = agent_skills_dir(repo_root, agent)
                if os.path.isdir(skills_dir):
                    for local_name in sorted(os.listdir(skills_dir)):
                        if local_name.startswith(SKILL_PREFIX) and local_name not in discovered_skills:
                            stale_path = os.path.join(skills_dir, local_name)
                            print(f"Removing obsolete upstream skill: agents/{agent}/skills/{local_name}...")
                            shutil.rmtree(stale_path)
                
            print("\nSyncing skills...")
            for skill_name in discovered_skills:
                src_skill_path = os.path.join(upstream_skills_dir, skill_name)
                agents = SKILL_AGENT_OVERRIDES.get(skill_name, DEFAULT_TARGET_AGENTS)
                
                for agent in agents:
                    dest_path = os.path.join(agent_skills_dir(repo_root, agent), skill_name)
                    print(f"Syncing '{skill_name}' to agents/{agent}/skills/{skill_name}...")
                    
                    # Delete existing destination directory to remove stale files
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                        
                    # Re-create destination parent directories if needed
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    # Copy from upstream src to dest
                    shutil.copytree(src_skill_path, dest_path)

                    # Apply in-place substitutions to correct upstream defects.
                    if apply_substitutions(dest_path, skill_name):
                        print(f"  Applied substitutions to {skill_name}/{SKILL_MD_FILENAME}")

                    # Re-inject the Cluster Agent coupling footer (wiped by the copy above).
                    if inject_footer(dest_path, skill_name):
                        print(f"  Injected kube-agents footer into {skill_name}/{SKILL_MD_FILENAME}")

            # Every mirrored file is now upstream content plus substitutions and footers, so the
            # override list starts empty again. Anything it held was just overwritten; name it so
            # the change can be re-made as a SKILL_SUBSTITUTIONS entry rather than lost quietly.
            for rel, reason in sorted(previous_overrides.items()):
                print(f"Wiped local override {rel} ({reason}); re-add it as a SKILL_SUBSTITUTIONS entry naming that file if still wanted.", file=sys.stderr)
            write_lock(repo_root, build_lock(repo_root, upstream_commit))
            print(f"Wrote {LOCK_FILE} at upstream commit {upstream_commit}.")

            print("\nSynchronization complete!")
    except subprocess.CalledProcessError:
        print("\nError: Synchronization failed due to command error. Details above.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
