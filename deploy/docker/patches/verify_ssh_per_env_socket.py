#!/usr/bin/env python3
"""Build gate for the per-environment SSH ControlMaster socket patch.

Run by ``deploy/docker/Dockerfile`` from ``/opt/hermes`` after
``apply_ssh_per_env_socket.py``. The applier proves its anchor matched once;
that says nothing about whether ``_session_id`` exists by the time the key is
built, or whether the sockets ``cleanup()`` closes are now only its own.

Two things are checked:

1. **Placement.** Parsed out of the patched ``tools/environments/ssh.py``: in
   ``SSHEnvironment.__init__`` the first ``socket_key`` assignment reads
   ``self._session_id``, sits in the method body rather than a branch, and comes
   after the ``super().__init__`` call; ``BaseEnvironment.__init__`` is what
   assigns ``self._session_id``.
2. **Behaviour.** Two real ``SSHEnvironment`` objects for one ``user@host:port``,
   with the steps that need a live sshd stubbed, get different plain and SendEnv
   sockets, and one's ``cleanup()`` sends ``-O exit`` to and unlinks its own
   sockets and none of the other's.

Usage::

    cd /opt/hermes && python3 verify_ssh_per_env_socket.py
"""

from __future__ import annotations

import ast
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FAILURES: list[str] = []

HERMES = Path(os.environ.get("HERMES_ROOT", "/opt/hermes"))

# Set before any Hermes import: modules resolve paths from the home at import
# time, and the build has no home of its own. SSHEnvironment puts its sockets
# under tempfile.gettempdir(), so that goes to the same scratch directory.
HOME = Path(tempfile.mkdtemp(prefix="verify-ssh-per-env-socket-"))
os.environ["HERMES_HOME"] = str(HOME)
tempfile.tempdir = str(HOME)

SSH_MODULE = Path("tools") / "environments" / "ssh.py"
BASE_MODULE = Path("tools") / "environments" / "base.py"
SSH_CLASS = "SSHEnvironment"
BASE_CLASS = "BaseEnvironment"
KEY_NAME = "socket_key"
SESSION_ID = "self._session_id"
CONTROL_PATH_OPTION = "ControlPath="
MARKER = "kube-agents patch: ssh-per-env-socket"

# Nothing connects, so any target will do; both environments get the same one.
TARGET = {"host": "sandbox.invalid", "user": "agent", "port": 2222}
REMOTE_HOME = "/home/agent"
SEND_ENV = ("HERMES_PROFILE_HOME",)


def check(label: str, condition: object, detail: str = "") -> None:
    if condition:
        print(f"  ok   {label}")
        return
    FAILURES.append(f"{label}{': ' + detail if detail else ''}")
    print(f"  FAIL {label}{': ' + detail if detail else ''}")


def _method(tree: ast.Module, cls: str, name: str):
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == cls]
    if len(classes) != 1:
        return None
    defs = [node for node in classes[0].body if isinstance(node, ast.FunctionDef) and node.name == name]
    return defs[0] if len(defs) == 1 else None


def _is_super_init(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and ast.unparse(stmt.value).startswith("super().__init__(")


def _assigns(node, target: str) -> list[ast.Assign]:
    if node is None:
        return []
    found = [
        child
        for child in ast.walk(node)
        if isinstance(child, ast.Assign) and [ast.unparse(t) for t in child.targets] == [target]
    ]
    return sorted(found, key=lambda child: child.lineno)


# --- 1. Placement -----------------------------------------------------------
print(f"socket key ({SSH_MODULE}):")

source = (HERMES / SSH_MODULE).read_text()
check("the patch marker is present exactly once", source.count(MARKER) == 1, f"found {source.count(MARKER)}")
init = _method(ast.parse(source), SSH_CLASS, "__init__")
keys = _assigns(init, KEY_NAME)
first_key = keys[0] if keys else None
check(
    f"the first {KEY_NAME} in {SSH_CLASS}.__init__ reads {SESSION_ID}",
    first_key is not None and SESSION_ID in ast.unparse(first_key.value),
    ast.unparse(first_key) if first_key else "no assignment found",
)
body = init.body if init else []
check(
    "and is in the method body, so it applies to every environment and not only a probe",
    first_key in body,
)
supers = [index for index, stmt in enumerate(body) if _is_super_init(stmt)]
check(
    "and follows the super().__init__ call that makes the session id",
    len(supers) == 1 and first_key in body and supers[0] < body.index(first_key),
    f"super().__init__ at {supers}",
)
base_init = _method(ast.parse((HERMES / BASE_MODULE).read_text()), BASE_CLASS, "__init__")
check(f"{BASE_CLASS}.__init__ assigns {SESSION_ID}", bool(_assigns(base_init, SESSION_ID)))


# --- 2. Behaviour -----------------------------------------------------------
print("behaviour:")

if str(HERMES) not in sys.path:
    sys.path.insert(0, str(HERMES))

from tools.environments import ssh  # noqa: E402


class _NoSync:
    def __init__(self, **_callbacks):
        pass

    def sync(self, **_options):
        pass

    def sync_back(self, *_args, **_options):
        pass


ssh._ensure_ssh_available = lambda: None
ssh.FileSyncManager = _NoSync
ssh.SSHEnvironment._establish_connection = lambda self: None
ssh.SSHEnvironment._detect_remote_home = lambda self: REMOTE_HOME
ssh.SSHEnvironment._ensure_remote_dirs = lambda self: None
ssh.SSHEnvironment.init_session = lambda self: None

first = ssh.SSHEnvironment(**TARGET)
second = ssh.SSHEnvironment(**TARGET)


def _sockets(env) -> set[Path]:
    return {Path(env.control_socket), env._control_socket_for(SEND_ENV)}


check(
    "two environments for one target get different plain sockets",
    first.control_socket != second.control_socket,
    str(first.control_socket),
)
check(
    "and different SendEnv sockets for the same names",
    first._control_socket_for(SEND_ENV) != second._control_socket_for(SEND_ENV),
)

# cleanup() only needs a socket path to exist, and finds the SendEnv siblings by
# globbing the directory, so regular files stand in for the sockets.
for env in (first, second):
    for path in _sockets(env):
        path.touch()

exited: list[Path] = []
real_run = subprocess.run


def _record(cmd, **_options):
    exited.extend(Path(arg[len(CONTROL_PATH_OPTION) :]) for arg in cmd if arg.startswith(CONTROL_PATH_OPTION))
    return subprocess.CompletedProcess(cmd, 0, b"", b"")


subprocess.run = _record
try:
    second.cleanup()
    check(
        "cleanup() sends -O exit to its own sockets and no others",
        set(exited) == _sockets(second) and len(exited) == len(_sockets(second)),
        f"sent to {sorted(map(str, exited))}",
    )
    check("and unlinks them", not any(path.exists() for path in _sockets(second)))
    check(
        "the other environment's sockets are still there",
        all(path.exists() for path in _sockets(first)),
    )
    first.cleanup()
    del first, second
finally:
    subprocess.run = real_run
    shutil.rmtree(HOME, ignore_errors=True)


print()
if FAILURES:
    print(f"verify_ssh_per_env_socket: {len(FAILURES)} FAILED")
    for f in FAILURES:
        print(f"  - {f}")
    sys.exit(1)
print("verify_ssh_per_env_socket: all checks passed")
