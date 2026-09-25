"""Give every Hermes SSH environment its own ControlMaster socket.

One anchored edit in ``tools/environments/ssh.py``: ``SSHEnvironment.__init__``
names its control socket after ``sha256(user@host:port)``, and the operator
publishes one host, one user and one port for the whole agent, so every
environment in every process in the agent pod — the gateway, the Platform Agent
worker, each Cluster Agent card — multiplexes over one master. ``cleanup()``
runs ``ssh -O exit`` on that path, which drops the master and every session
riding it, so a worker finishing its card cuts a sibling's in-flight command:
exit 255, empty output. The idle reaper is kept out of that by the operator's
30-day ``terminal.lifetime_seconds``; a worker process exiting is not.

The edit appends the environment's ``_session_id`` (set by
``BaseEnvironment.__init__``, which runs first) to the socket key, so each
environment's master is its own and its teardown can only close that. The
SendEnv sibling sockets are derived from the plain socket's name, and
``cleanup()`` finds them by its prefix, so they follow without an edit. The probe
branch below the edited line still appends its own suffix and stays distinct.

Upstream already keys the prompt-time probe per instance. When a base bump moves
this line, check whether upstream now keys every environment that way; if it
does, delete this patch rather than re-deriving the anchor.
"""

from __future__ import annotations

import sys
from pathlib import Path

import patchlib

SSH_RELATIVE = "tools/environments/ssh.py"

# The whole line, newline included, so a longer key that begins the same way
# cannot stand in for it. The probe branch's reassignment does not match.
KEY_LINE = 'socket_key = f"{user}@{host}:{port}"\n'

MARKER = "kube-agents patch: ssh-per-env-socket"

PER_ENV_KEY_LINE = f'socket_key = f"{{user}}@{{host}}:{{port}}:{{self._session_id}}"  # {MARKER}\n'


def apply(root: Path) -> None:
    patch = patchlib.Patch(root, SSH_RELATIVE, prefix="ssh-per-env-socket")
    patch.refuse_if_patched(MARKER)
    patch.substitute(KEY_LINE, PER_ENV_KEY_LINE, label="ControlPath socket key")
    patch.commit("ControlPath socket keyed per environment")


if __name__ == "__main__":
    apply(Path(sys.argv[1] if len(sys.argv) > 1 else "/opt/hermes"))
