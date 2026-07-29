"""Unit tests for the no-LLM GitHub issue poll gate.

Run: python3 -m unittest agents/chat/scripts/test_github_issue_gate.py

Covers the deterministic decision logic of github_issue_gate.py: when it files a
triage card, when it stays silent, and when it is allowed to speak.

The distinction that matters most here is silence vs. fault. "No issues" and "I
am broken" both produce no cards, and if they also both produce no output then a
resolver that stops working looks exactly like a quiet repository — forever. So
the fault paths are asserted to speak, and the quiet paths to say nothing.
"""

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.absolute()))

import github_issue_gate  # noqa: E402

ALERT = github_issue_gate.ALERT_STATE_FILE


class RepoConfiguredTest(unittest.TestCase):
    """An operator with no GitOps repo is a supported state, not a fault."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_false_when_settings_missing(self):
        self.assertFalse(github_issue_gate.repo_configured(str(self.d / "nope.md")))

    def test_false_when_key_absent(self):
        p = self.d / "SETTINGS.md"
        p.write_text("- **Project:** toshiowang-gkedemos\n", encoding="utf-8")
        self.assertFalse(github_issue_gate.repo_configured(str(p)))

    def test_true_when_key_present(self):
        p = self.d / "SETTINGS.md"
        p.write_text(
            "- **Git Repo:** https://github.com/gke-labs/kube-agents.git\n",
            encoding="utf-8",
        )
        self.assertTrue(github_issue_gate.repo_configured(str(p)))


class RunPollTest(unittest.TestCase):
    """run_poll must classify every resolver outcome, never raise."""

    def setUp(self):
        self._orig = subprocess.run

    def tearDown(self):
        subprocess.run = self._orig

    def _stub(self, returncode=0, stdout="", stderr=""):
        def fake(*a, **kw):
            return subprocess.CompletedProcess(a[0], returncode, stdout, stderr)

        subprocess.run = fake

    def test_parses_found(self):
        self._stub(stdout=json.dumps({"status": "FOUND", "issue_number": 7}))
        payload, fault = github_issue_gate.run_poll("/x/resolver.py")
        self.assertIsNone(fault)
        self.assertEqual(payload["status"], "FOUND")

    def test_nonzero_exit_is_a_fault(self):
        # The pre-#460 resolver sys.exit(1)s on a bad auth pre-flight; whatever
        # the cause, a crashed poll must not read as "nothing to triage".
        self._stub(returncode=1, stderr="Error: gh auth failed")
        payload, fault = github_issue_gate.run_poll("/x/resolver.py")
        self.assertIsNone(payload)
        self.assertEqual(fault, "POLL_EXITED_1")

    def test_unparseable_stdout_is_a_fault(self):
        self._stub(stdout="Traceback (most recent call last):\n")
        _, fault = github_issue_gate.run_poll("/x/resolver.py")
        self.assertEqual(fault, "POLL_OUTPUT_UNPARSEABLE")

    def test_valid_json_without_status_is_a_fault(self):
        self._stub(stdout=json.dumps(["not", "a", "payload"]))
        _, fault = github_issue_gate.run_poll("/x/resolver.py")
        self.assertEqual(fault, "POLL_OUTPUT_UNPARSEABLE")

    def test_timeout_is_a_fault_not_an_exception(self):
        def fake(*a, **kw):
            raise subprocess.TimeoutExpired(a[0], 120)

        subprocess.run = fake
        payload, fault = github_issue_gate.run_poll("/x/resolver.py")
        self.assertIsNone(payload)
        self.assertEqual(fault, "POLL_TIMED_OUT")


class GateTestBase(unittest.TestCase):
    """Stubs out everything outside the gate: the resolver, the board, settings."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)
        self.filed = []

        self._orig_file = github_issue_gate.file_issue_task
        self._orig_path = github_issue_gate.resolver_path
        self._orig_repo = github_issue_gate.repo_configured
        self._orig_poll = github_issue_gate.run_poll

        github_issue_gate.file_issue_task = lambda repo, num: self.filed.append((repo, num))
        github_issue_gate.resolver_path = lambda: "/x/resolver.py"
        github_issue_gate.repo_configured = lambda *a, **kw: True

    def tearDown(self):
        github_issue_gate.file_issue_task = self._orig_file
        github_issue_gate.resolver_path = self._orig_path
        github_issue_gate.repo_configured = self._orig_repo
        github_issue_gate.run_poll = self._orig_poll
        self._tmp.cleanup()

    def _poll(self, payload=None, fault=None):
        github_issue_gate.run_poll = lambda script: (payload, fault)

    def _run(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = github_issue_gate.main(self.d)
        return rc, buf.getvalue().strip()


class MainTest(GateTestBase):
    def test_files_card_when_issue_found(self):
        self._poll({"status": "FOUND", "repository": "acme/toolkit", "issue_number": 42})
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertEqual(self.filed, [("acme/toolkit", 42)])
        self.assertEqual(out, "")  # the triage worker speaks, not this job

    def test_silent_no_card_when_no_issues(self):
        self._poll({"status": "NO_ISSUES", "repository": "acme/toolkit"})
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertEqual(self.filed, [])
        self.assertEqual(out, "")

    def test_skips_entirely_when_resolver_absent(self):
        # A deployment without the skill installed must degrade silently rather
        # than nag an operator who never asked for issue triage.
        github_issue_gate.resolver_path = lambda: None
        self._poll({"status": "FOUND", "repository": "a/b", "issue_number": 1})
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertEqual(self.filed, [])
        self.assertEqual(out, "")

    def test_skips_entirely_when_no_repo_configured(self):
        github_issue_gate.repo_configured = lambda *a, **kw: False
        self._poll({"status": "FOUND", "repository": "a/b", "issue_number": 1})
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertEqual(self.filed, [])
        self.assertEqual(out, "")

    def test_found_without_usable_fields_files_nothing(self):
        self._poll({"status": "FOUND", "repository": "acme/toolkit"})
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertEqual(self.filed, [])
        self.assertEqual(out, "")

    def test_string_issue_number_is_coerced(self):
        # gh returns an int today, but dropping a real issue over its JSON type
        # would be a silent triage outage.
        self._poll({"status": "FOUND", "repository": "a/b", "issue_number": "9"})
        self._run()
        self.assertEqual(self.filed, [("a/b", 9)])

    def test_kanban_failure_is_survivable(self):
        # file_issue_task swallows board errors and returns None; the issue stays
        # unlabeled, so the next tick simply re-polls it.
        def boom(repo, num):
            return None

        github_issue_gate.file_issue_task = boom
        self._poll({"status": "FOUND", "repository": "a/b", "issue_number": 3})
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")


class FaultAlertTest(GateTestBase):
    """A broken resolver must be loud once — not silent, and not twelve times an hour."""

    def test_poll_fault_alerts(self):
        self._poll(fault="POLL_EXITED_1")
        rc, out = self._run()
        self.assertEqual(rc, 0)
        self.assertIn("GitHub issue resolver is not running", out)
        self.assertIn("POLL_EXITED_1", out)

    def test_error_status_alerts_with_its_reason(self):
        self._poll({"status": "ERROR", "reason": "GITHUB_AUTH_NOT_CONFIGURED"})
        _, out = self._run()
        self.assertIn("GITHUB_AUTH_NOT_CONFIGURED", out)
        self.assertEqual(self.filed, [])

    def test_same_fault_is_announced_only_once(self):
        self._poll(fault="POLL_EXITED_1")
        _, first = self._run()
        _, second = self._run()
        self.assertNotEqual(first, "")
        self.assertEqual(second, "")

    def test_a_different_fault_is_announced_again(self):
        self._poll(fault="POLL_EXITED_1")
        self._run()
        self._poll(fault="POLL_TIMED_OUT")
        _, out = self._run()
        self.assertIn("POLL_TIMED_OUT", out)

    def test_recovery_clears_the_alert_so_a_relapse_speaks(self):
        self._poll(fault="POLL_EXITED_1")
        self._run()
        self.assertTrue((self.d / ALERT).exists())

        self._poll({"status": "NO_ISSUES", "repository": "a/b"})
        self._run()
        self.assertFalse((self.d / ALERT).exists())

        self._poll(fault="POLL_EXITED_1")
        _, out = self._run()
        self.assertIn("POLL_EXITED_1", out)

    def test_error_status_does_not_clear_the_alert(self):
        # ERROR means the resolver ran but cannot work. Treating that as a
        # recovery would re-announce the same fault on the very next tick.
        self._poll({"status": "ERROR", "reason": "GITHUB_AUTH_NOT_CONFIGURED"})
        self._run()
        _, second = self._run()
        self.assertEqual(second, "")


class TaskBodyTest(unittest.TestCase):
    """The card is the worker's whole brief; the safety contract has to survive in it."""

    def setUp(self):
        self.body = github_issue_gate._task_body("acme/toolkit", 42)

    def test_directs_the_worker_past_the_already_completed_poll(self):
        self.assertIn("Skip Step 1", self.body)
        self.assertIn("claim --issue 42", self.body)

    def test_carries_the_red_line_forward(self):
        # The labels are filtered at poll time, but a card can sit on the board
        # long enough for the issue to be escalated underneath it.
        self.assertIn("status:escalation-needed", self.body)
        self.assertIn("agent:ignore", self.body)

    def test_marks_issue_content_as_untrusted(self):
        self.assertIn("untrusted", self.body)

    def test_pins_the_documented_report_path(self):
        self.assertIn("/opt/data/scratch/report_42.md", self.body)

    def test_assignee_is_the_privileged_specialist(self):
        # The Chat Agent profile this cron runs on holds no terminal, kubectl, or
        # gcloud, so triage cannot happen here at any cost.
        self.assertEqual(github_issue_gate.TASK_ASSIGNEE, "platform")


if __name__ == "__main__":
    unittest.main()
