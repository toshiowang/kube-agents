"""Unit tests for scripts/sync-upstream-skills.py.

Run: python3 -m unittest scripts.test_sync_upstream_skills

Two invariants: after an upstream sync wipes a skill dir, substitutions and the footer are
re-applied exactly once (idempotent) and only for skills that have them; and every mirrored file
in the tree matches scripts/upstream_skills_lock.json or is listed there as a local override.
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

# The module file name has hyphens, so load it by path rather than a plain import.
_SPEC = importlib.util.spec_from_file_location(
    "sync_upstream_skills", str(Path(__file__).resolve().parent / "sync-upstream-skills.py")
)
sync = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(sync)


class InjectFooterTest(unittest.TestCase):
    def _skill_dir(self, body="# Upstream skill\n\nSome content.\n"):
        d = Path(tempfile.mkdtemp())
        (d / "SKILL.md").write_text(body, encoding="utf-8")
        return d

    def _read(self, d):
        return (d / "SKILL.md").read_text(encoding="utf-8")

    def test_injects_footer_for_configured_skill(self):
        d = self._skill_dir()
        self.assertTrue(sync.inject_footer(str(d), "gke-cluster-creation"))
        text = self._read(d)
        self.assertIn(sync.FOOTER_MARKER, text)
        self.assertIn("provision the Cluster Agent profile", text)
        self.assertIn("cluster_agent_profile.py create", text)

    def test_creation_footer_covers_teardown(self):
        d = self._skill_dir()
        self.assertTrue(sync.inject_footer(str(d), "gke-cluster-creation"))
        text = self._read(d)
        self.assertIn("Cluster Agent Profile Teardown", text)
        self.assertIn("cluster_agent_profile.py delete", text)
        self.assertIn("cluster-agent-reconcile", text)

    def test_idempotent_no_duplicate(self):
        d = self._skill_dir()
        self.assertTrue(sync.inject_footer(str(d), "gke-cluster-creation"))
        # Second call must be a no-op (footer already present from this run's copy).
        self.assertFalse(sync.inject_footer(str(d), "gke-cluster-creation"))
        self.assertEqual(self._read(d).count(sync.FOOTER_MARKER), 1)

    def test_unconfigured_skill_untouched(self):
        d = self._skill_dir(body="original\n")
        self.assertFalse(sync.inject_footer(str(d), "gke-cost-analysis"))
        self.assertEqual(self._read(d), "original\n")

    def test_missing_skill_md_is_safe(self):
        d = Path(tempfile.mkdtemp())  # no SKILL.md
        self.assertFalse(sync.inject_footer(str(d), "gke-cluster-creation"))


class ApplySubstitutionsTest(unittest.TestCase):
    def test_three_tuple_targets_a_file_inside_the_skill(self):
        d = Path(tempfile.mkdtemp())
        (d / "SKILL.md").write_text("body\n", encoding="utf-8")
        (d / "references").mkdir()
        (d / "references" / "notes.md").write_text("old text\n", encoding="utf-8")
        original = sync.SKILL_SUBSTITUTIONS
        sync.SKILL_SUBSTITUTIONS = {"gke-x": [("references/notes.md", "old text", "new text")]}
        try:
            self.assertTrue(sync.apply_substitutions(str(d), "gke-x"))
            self.assertEqual((d / "references" / "notes.md").read_text(encoding="utf-8"), "new text\n")
            self.assertEqual((d / "SKILL.md").read_text(encoding="utf-8"), "body\n")
            self.assertFalse(sync.apply_substitutions(str(d), "gke-x"))
        finally:
            sync.SKILL_SUBSTITUTIONS = original

    def _skill_dir(self, body=""):
        d = Path(tempfile.mkdtemp())
        (d / sync.SKILL_MD_FILENAME).write_text(body, encoding=sync.UTF_8_ENCODING)
        return d

    def _read(self, d):
        return (d / sync.SKILL_MD_FILENAME).read_text(encoding=sync.UTF_8_ENCODING)

    def test_applies_substitution_for_configured_skill(self):
        d = self._skill_dir(body=sync.GKE_WORKLOAD_SECURITY_OLD_NETPOL_SNIPPET + "\n")
        self.assertTrue(sync.apply_substitutions(str(d), "gke-workload-security"))
        text = self._read(d)
        self.assertNotIn(sync.GKE_WORKLOAD_SECURITY_OLD_NETPOL_SNIPPET, text)
        self.assertIn(sync.GKE_WORKLOAD_SECURITY_NEW_NETPOL_SNIPPET, text)
        self.assertIn("--enable-network-policy", text)

    def test_idempotent_no_duplicate(self):
        d = self._skill_dir(body=sync.GKE_WORKLOAD_SECURITY_OLD_NETPOL_SNIPPET + "\n")
        self.assertTrue(sync.apply_substitutions(str(d), "gke-workload-security"))
        # Second call must be a no-op (replacement already present).
        self.assertFalse(sync.apply_substitutions(str(d), "gke-workload-security"))
        text = self._read(d)
        self.assertEqual(text.count(sync.GKE_WORKLOAD_SECURITY_NEW_NETPOL_SNIPPET), 1)

    def test_unconfigured_skill_untouched(self):
        d = self._skill_dir(body="original\n")
        self.assertFalse(sync.apply_substitutions(str(d), "gke-cost-analysis"))
        self.assertEqual(self._read(d), "original\n")

    def test_missing_skill_md_is_safe(self):
        d = Path(tempfile.mkdtemp())  # no SKILL.md
        self.assertFalse(sync.apply_substitutions(str(d), "gke-workload-security"))

    def test_target_not_found_returns_false(self):
        d = self._skill_dir(body="other content\n")
        self.assertFalse(sync.apply_substitutions(str(d), "gke-workload-security"))
        self.assertEqual(self._read(d), "other content\n")

    def test_repo_workload_security_skills_have_enforcement_command(self):
        repo_root = Path(__file__).resolve().parent.parent
        for agent in ["platform", "cluster"]:
            skill_md = repo_root / "agents" / agent / "skills" / "gke-workload-security" / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"{skill_md} must exist")
            content = skill_md.read_text(encoding="utf-8")
            self.assertIn("--enable-network-policy", content)
            self.assertIn("--update-addons=NetworkPolicy=ENABLED", content)
            self.assertIn("networkConfig.datapathProvider", content)
            self.assertIn("--location <location>", content)
            self.assertIn("node pools may be recreated; this can take several minutes", content)
            self.assertNotIn(sync.GKE_WORKLOAD_SECURITY_OLD_NETPOL_SNIPPET, content)
            self.assertIn(sync.GKE_WORKLOAD_SECURITY_NEW_NETPOL_SNIPPET, content)

class MirrorLockTest(unittest.TestCase):
    """The tree's mirrored files match scripts/upstream_skills_lock.json.

    Mirrored (`gke-*`) skill directories are rewritten wholesale by the sync, so an edit made
    directly to one lasts until the next run. These tests make that edit fail here instead:
    every mirrored file must digest to what the last sync wrote, or be named under
    local_overrides with the pull request that changed it.
    """

    REPO_ROOT = Path(__file__).resolve().parent.parent
    SHA1_HEX_LENGTH = 40

    def _fake_repo(self, body="upstream\n"):
        root = Path(tempfile.mkdtemp())
        skill = root / "agents" / "platform" / "skills" / "gke-example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(body, encoding="utf-8")
        (root / "scripts").mkdir()
        return root, skill / "SKILL.md"

    def test_repo_mirrors_match_lock(self):
        problems = sync.check_lock(str(self.REPO_ROOT), sync.load_lock(str(self.REPO_ROOT)))
        self.assertEqual(
            problems,
            [],
            "\n".join(
                [
                    "Mirrored gke-* skill files differ from the last upstream sync:",
                    *problems,
                    "These directories are rewritten by scripts/sync-upstream-skills.py, so a direct edit",
                    "is lost at the next run. Put the change in SKILL_SUBSTITUTIONS or SKILL_FOOTERS there",
                    "and rerun the sync (it reads the pinned commit by default and rewrites the lock).",
                    f"local_overrides in {sync.LOCK_FILE} records deviations already merged, which the",
                    "next sync wipes; it is not where a new change goes.",
                ]
            ),
        )

    def test_lock_pins_an_upstream_commit(self):
        lock = sync.load_lock(str(self.REPO_ROOT))
        commit = lock[sync.LOCK_COMMIT_KEY]
        self.assertEqual(len(commit), self.SHA1_HEX_LENGTH)
        int(commit, 16)
        self.assertEqual(lock[sync.LOCK_REPO_KEY], sync.UPSTREAM_REPO)

    def test_direct_edit_is_a_problem_until_listed_as_an_override(self):
        root, skill_md = self._fake_repo()
        lock = sync.build_lock(str(root), "0" * self.SHA1_HEX_LENGTH)
        self.assertEqual(sync.check_lock(str(root), lock), [])

        skill_md.write_text("edited locally\n", encoding="utf-8")
        problems = sync.check_lock(str(root), lock)
        self.assertEqual(len(problems), 1)
        self.assertIn("differs from the last sync", problems[0])

        rel = str(skill_md.relative_to(root))
        lock[sync.LOCK_OVERRIDES_KEY] = {rel: "#1: reason"}
        self.assertEqual(sync.check_lock(str(root), lock), [])

    def test_stale_override_and_unsynced_file_are_problems(self):
        root, skill_md = self._fake_repo()
        rel = str(skill_md.relative_to(root))
        lock = sync.build_lock(str(root), "0" * self.SHA1_HEX_LENGTH, {rel: "#1: reason"})
        problems = sync.check_lock(str(root), lock)
        self.assertEqual(len(problems), 1)
        self.assertIn("stale entry", problems[0])

        lock[sync.LOCK_OVERRIDES_KEY] = {}
        (skill_md.parent / "references").mkdir()
        (skill_md.parent / "references" / "new.md").write_text("x\n", encoding="utf-8")
        problems = sync.check_lock(str(root), lock)
        self.assertEqual(len(problems), 1)
        self.assertIn("added outside the sync", problems[0])

    def test_hidden_files_are_not_part_of_the_mirror(self):
        root, skill_md = self._fake_repo()
        lock = sync.build_lock(str(root), "0" * self.SHA1_HEX_LENGTH)
        (skill_md.parent / ".DS_Store").write_bytes(b"\x00")
        self.assertEqual(sync.check_lock(str(root), lock), [])

    def test_lock_round_trips_through_the_file(self):
        root, _ = self._fake_repo()
        lock = sync.build_lock(str(root), "0" * self.SHA1_HEX_LENGTH)
        sync.write_lock(str(root), lock)
        self.assertEqual(sync.load_lock(str(root)), lock)


if __name__ == "__main__":
    unittest.main()
