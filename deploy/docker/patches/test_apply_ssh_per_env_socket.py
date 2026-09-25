"""Unit tests for apply_ssh_per_env_socket.py against a miniature tools/environments/ssh.py.

Run: python3 -m unittest discover -s deploy/docker/patches -p 'test_*.py' -t deploy/docker/patches

The real file is asserted against the shipped image by verify_ssh_per_env_socket.py;
these tests cover the applier's own contract: it rewrites the one key line, leaves
the probe branch alone, and refuses anything else.
"""

import ast
import importlib.util
import tempfile
import unittest
from pathlib import Path

from apply_ssh_per_env_socket import KEY_LINE, MARKER, PER_ENV_KEY_LINE, SSH_RELATIVE, apply

BODY_INDENT = " " * 8
PROBE_LINE = 'socket_key = f"{socket_key}:probe:{self._session_id}"\n'
TARGET = {"host": "sandbox.invalid", "user": "agent", "port": 2222}

# The shape of SSHEnvironment's socket naming at v2026.9.14, with the base class
# reduced to the session id it assigns.
SSH_STUB = '''import hashlib
import tempfile
import uuid
from pathlib import Path


class BaseEnvironment:
    def __init__(self, cwd, timeout):
        self._session_id = uuid.uuid4().hex[:12]


class SSHEnvironment(BaseEnvironment):
    def __init__(self, host, user, cwd="~", timeout=60, port=22, key_path="", probe_only=False):
        super().__init__(cwd=cwd, timeout=timeout)
        self.control_dir = Path(tempfile.gettempdir()) / "hermes-ssh"
        socket_key = f"{user}@{host}:{port}"
        if probe_only:
            socket_key = f"{socket_key}:probe:{self._session_id}"
        _socket_id = hashlib.sha256(socket_key.encode()).hexdigest()[:16]
        self.control_socket = self.control_dir / f"{_socket_id}.sock"
'''


def stage(source=SSH_STUB):
    root = Path(tempfile.mkdtemp())
    path = root / SSH_RELATIVE
    path.parent.mkdir(parents=True)
    path.write_text(source)
    return root


def load(root, name):
    spec = importlib.util.spec_from_file_location(name, root / SSH_RELATIVE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ApplierTest(unittest.TestCase):
    def test_the_key_gains_the_session_id_and_the_file_stays_parseable(self):
        root = stage()
        apply(root)
        patched = (root / SSH_RELATIVE).read_text()
        ast.parse(patched)
        self.assertIn(BODY_INDENT + PER_ENV_KEY_LINE, patched)
        self.assertEqual(patched.count(MARKER), 1)

    def test_only_the_key_line_changes(self):
        root = stage()
        apply(root)
        patched = (root / SSH_RELATIVE).read_text()
        self.assertEqual(
            patched.replace(PER_ENV_KEY_LINE, KEY_LINE, 1),
            SSH_STUB,
            "the applier changed something other than the one key line",
        )

    def test_the_probe_branch_is_left_alone(self):
        root = stage()
        apply(root)
        self.assertIn(BODY_INDENT + " " * 4 + PROBE_LINE, (root / SSH_RELATIVE).read_text())

    def test_two_environments_for_one_target_get_different_sockets(self):
        """The point of the patch; the unpatched stub is the control that shows the test can fail."""
        unpatched = load(stage(), "unpatched_ssh")
        self.assertEqual(
            unpatched.SSHEnvironment(**TARGET).control_socket,
            unpatched.SSHEnvironment(**TARGET).control_socket,
        )
        root = stage()
        apply(root)
        patched = load(root, "patched_ssh")
        self.assertNotEqual(
            patched.SSHEnvironment(**TARGET).control_socket,
            patched.SSHEnvironment(**TARGET).control_socket,
        )

    def test_a_missing_key_line_is_fatal_not_silent(self):
        root = stage(SSH_STUB.replace(BODY_INDENT + KEY_LINE, ""))
        with self.assertRaises(SystemExit) as ctx:
            apply(root)
        self.assertIn("found 0", str(ctx.exception))

    def test_a_key_line_that_grew_is_fatal(self):
        """A base that already changed the key needs a look, not a second suffix."""
        grown = SSH_STUB.replace(KEY_LINE, 'socket_key = f"{user}@{host}:{port}:{self._session_id}"\n')
        self.assertNotEqual(grown, SSH_STUB)
        with self.assertRaises(SystemExit) as ctx:
            apply(stage(grown))
        self.assertIn("found 0", str(ctx.exception))

    def test_two_key_lines_are_fatal(self):
        doubled = SSH_STUB.replace(BODY_INDENT + KEY_LINE, (BODY_INDENT + KEY_LINE) * 2)
        self.assertNotEqual(doubled, SSH_STUB)
        with self.assertRaises(SystemExit) as ctx:
            apply(stage(doubled))
        self.assertIn("found 2", str(ctx.exception))

    def test_applying_twice_is_refused(self):
        root = stage()
        apply(root)
        with self.assertRaises(SystemExit) as ctx:
            apply(root)
        self.assertIn("already patched", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
