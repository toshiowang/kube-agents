# Copyright 2026 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The ``card_tool_called`` verifier, over a local agent data volume.

The board read and the worker-session read both run their in-pod scripts
here, through the real command lines, against a board and session stores in
hermes' shapes in a temporary directory, as ``test_worker_trajectory.py``
builds them.
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import pytest
import yaml
from devops_bench.verification.base import VERIFIERS
from devops_bench.verification.spec import parse_node

from kube_agents_bench import board, onboarding, worker_trajectory
from kube_agents_bench.verifiers import CardToolCalledVerifier

REPO = Path(__file__).resolve().parents[2]
TASK = REPO / "bench" / "tasks" / "bootstrap-inventory-ranking-delivery" / "task.yaml"
REDACTOR = REPO / "agents" / "chat" / "defaults" / "plugins" / "common" / "redactor.py"

KEY = "bootstrap-inventory-prioritize"
CARD = "t_prio0001"
EARLIER = "t_prio0000"
CHILD = "t_child001"
CARD_SESSION = "20260929_220000_aaaaaa"
EARLIER_SESSION = "20260928_220000_bbbbbb"
CHILD_SESSION = "20260929_221000_cccccc"
TOOL = "mcp_platform_control_register_inventory_scores"
WRAPPED_TOOL = "mcp__platform_control__register_inventory_scores"
OK = json.dumps({"registered": 6, "ranked": []})
FAILED = json.dumps({"ok": False, "error": "INVENTORY.scores.json is missing ids f003"})

_BOARD_DDL = (
    "CREATE TABLE tasks (id TEXT PRIMARY KEY, title TEXT, assignee TEXT, status TEXT,"
    " created_by TEXT, created_at INTEGER, idempotency_key TEXT)",
    "CREATE TABLE task_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT,"
    " profile TEXT, status TEXT, started_at INTEGER, ended_at INTEGER, summary TEXT,"
    " metadata TEXT)",
    "CREATE TABLE task_links (parent_id TEXT, child_id TEXT, PRIMARY KEY (parent_id, child_id))",
    "CREATE TABLE kanban_worker_children (child_id TEXT PRIMARY KEY, creator_id TEXT, created_at INTEGER)",
)
_STORE_DDL = (
    "CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, role TEXT,"
    " content TEXT, tool_call_id TEXT, tool_calls TEXT, tool_name TEXT, timestamp REAL,"
    " active INTEGER DEFAULT 1)",
    "CREATE TABLE sessions (id TEXT PRIMARY KEY, input_tokens INTEGER NOT NULL DEFAULT 0,"
    " output_tokens INTEGER NOT NULL DEFAULT 0, cache_read_tokens INTEGER NOT NULL DEFAULT 0,"
    " cache_write_tokens INTEGER NOT NULL DEFAULT 0, reasoning_tokens INTEGER NOT NULL DEFAULT 0)",
)


def _call(name: str, args: dict[str, Any], result: str) -> list[tuple]:
    """One assistant tool call and its result, in hermes' flat stored shape."""
    return [
        ("assistant", None, [{"name": name, "arguments": json.dumps(args)}]),
        ("tool", result, None),
    ]


def _session(root: Path, session: str, task: str, calls: list[tuple]) -> None:
    path = root / "profiles" / "platform" / "state.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        for ddl in _STORE_DDL:
            conn.execute(ddl.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1))
        conn.execute("INSERT INTO sessions (id, input_tokens) VALUES (?, 1)", (session,))
        messages = [("user", f"work kanban task {task}", None), *calls, ("assistant", "Done.", None)]
        for index, (role, content, tool_calls) in enumerate(messages):
            conn.execute(
                "INSERT INTO messages (session_id, role, content, tool_calls, timestamp) VALUES (?, ?, ?, ?, ?)",
                (session, role, content, json.dumps(tool_calls) if tool_calls else None, 1000.0 + index),
            )


def _card(root: Path, task: str, key: str, created: int, session: str | None, *, parent: str | None = None) -> None:
    with sqlite3.connect(root / board.BOARD_FILE) as conn:
        for ddl in _BOARD_DDL:
            conn.execute(ddl.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1))
        conn.execute(
            "INSERT INTO tasks VALUES (?, 'Prioritize the onboarding inventory report', 'platform', 'done', 'platform', ?, ?)",
            (task, created, key),
        )
        metadata = json.dumps({"worker_session_id": session} if session else {})
        conn.execute(
            "INSERT INTO task_runs (task_id, profile, status, started_at, ended_at, metadata)"
            " VALUES (?, 'platform', 'done', 1, 2, ?)",
            (task, metadata),
        )
        if parent:
            conn.execute("INSERT INTO kanban_worker_children VALUES (?, ?, 1)", (task, parent))


def _local_shell(script: str, timeout: float) -> str:
    return subprocess.run(["sh", "-c", script], capture_output=True, text=True, timeout=timeout, check=True).stdout


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The agent's data volume, read through the real command lines run locally."""
    if not REDACTOR.exists():
        pytest.skip(f"{REDACTOR} is not beside this checkout")
    for module in (board, worker_trajectory):
        monkeypatch.setattr(module, "DATA_ROOT", str(tmp_path))
        monkeypatch.setattr(module, "HERMES_PYTHON", sys.executable)
    monkeypatch.setattr(worker_trajectory, "REDACTOR_PATH", str(REDACTOR))
    monkeypatch.setattr(onboarding, "agent_shell", _local_shell)
    return tmp_path


def _objective() -> dict[str, Any]:
    spec = yaml.safe_load(TASK.read_text().split("\n---\n", 1)[1])["verification_spec"]
    return next(e for e in spec if e["name"] == "worker-called-the-tool")["check"]


def _verify(timeout: float = 0.0, **overrides: Any):
    return CardToolCalledVerifier(**{**_objective(), **overrides}).verify(timeout)


def test_a_call_by_the_cards_worker_passes(root: Path) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call("terminal", {"command": "ls"}, "ok") + _call(TOOL, {}, OK))
    result = _verify()
    assert result.status == "pass", result.reason
    assert f"card {CARD} (done): its worker made 1 call(s)" in result.reason


def test_a_call_inside_a_tool_call_wrapper_passes(root: Path) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call("tool_call", {"calls": [{"name": WRAPPED_TOOL, "arguments": {}}]}, OK))
    result = _verify()
    assert result.status == "pass", result.reason


def test_a_failed_call_fails_when_success_is_required(root: Path) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call(TOOL, {}, FAILED))
    result = _verify()
    assert result.status == "fail", result.reason
    assert f"it called ['{TOOL}']" in result.reason
    assert _verify(require_success=False).status == "pass"


def test_no_call_to_the_tool_fails_and_names_what_was_called(root: Path) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call("terminal", {"command": "python3 inventory_findings.py register"}, "ok"))
    result = _verify()
    assert result.status == "fail"
    assert "it called ['terminal']" in result.reason


def test_the_newest_card_with_the_key_is_the_one_read(root: Path) -> None:
    """An earlier run's archived card, whose worker did call the tool, does not count."""
    _card(root, EARLIER, KEY, 100, EARLIER_SESSION)
    _session(root, EARLIER_SESSION, EARLIER, _call(TOOL, {}, OK))
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call("terminal", {"command": "ls"}, "ok"))
    result = _verify()
    assert result.status == "fail"
    assert f"card {CARD}" in result.reason


def test_a_call_by_a_card_the_worker_filed_does_not_count(root: Path) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call("kanban_create", {"title": "register"}, json.dumps({"id": CHILD})))
    _card(root, CHILD, "", 300, CHILD_SESSION, parent=CARD)
    _session(root, CHILD_SESSION, CHILD, _call(TOOL, {}, OK))
    captured = worker_trajectory.capture(_local_shell, [CARD], 5.0)
    assert [(e["task"], e["name"]) for e in captured.entries] == [(CARD, "kanban_create"), (CHILD, TOOL)]
    result = _verify()
    assert result.status == "fail", result.reason
    assert "it called ['kanban_create']" in result.reason


def test_too_few_calls_in_a_read_with_gaps_is_an_error(root: Path) -> None:
    """A filed card with no session is a gap: the missing call may be there."""
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, _call("kanban_create", {"title": "register"}, json.dumps({"id": CHILD})))
    _card(root, CHILD, "", 300, None, parent=CARD)
    assert worker_trajectory.gaps(worker_trajectory.capture(_local_shell, [CARD], 5.0).summary)
    result = _verify()
    assert result.status == "error", result.reason
    assert "could not read" in result.reason


def test_a_worker_with_no_call_read_is_an_error(root: Path) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    _session(root, CARD_SESSION, CARD, [])
    result = _verify()
    assert result.status == "error"
    assert "the read found no call by its worker" in result.reason


def test_no_card_with_the_key_fails(root: Path) -> None:
    _card(root, CARD, "some-other-key", 200, CARD_SESSION)
    result = _verify()
    assert result.status == "fail"
    assert f"no card on the board has idempotency key '{KEY}'" in result.reason


def test_an_unreadable_board_is_an_error(root: Path) -> None:
    assert _verify().status == "error"


def test_an_unreadable_session_store_is_an_error(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _card(root, CARD, KEY, 200, CARD_SESSION)
    monkeypatch.setattr(worker_trajectory, "capture", lambda shell, ids, timeout: None)
    result = _verify()
    assert result.status == "error"
    assert "its worker sessions could not be read" in result.reason


# --- registration ---------------------------------------------------------


def test_the_verifier_is_published_as_an_entry_point() -> None:
    with (REPO / "bench" / "pyproject.toml").open("rb") as fh:
        eps = tomllib.load(fh)["project"]["entry-points"]["devops_bench.verifiers"]
    assert eps["card_tool_called"] == "kube_agents_bench.verifiers:CardToolCalledVerifier"


def test_parse_node_builds_the_case_objective() -> None:
    node = parse_node(_objective())
    assert isinstance(node, CardToolCalledVerifier)
    assert VERIFIERS.get("card_tool_called") is CardToolCalledVerifier
    assert node.idempotency_key == KEY
    assert set(node.tool_names) == {TOOL, WRAPPED_TOOL}


def test_the_case_names_the_key_the_stack_files() -> None:
    main_tf = (REPO / "bench" / "tf" / "prebuilt" / "bootstrap-ranking" / "main.tf").read_text()
    assert f'card_key      = "{_objective()["idempotency_key"]}"' in main_tf


@pytest.mark.parametrize(
    "check",
    [{"idempotency_key": "", "tool_names": [TOOL]}, {"idempotency_key": KEY, "tool_names": []}, {"tool_names": [TOOL]}],
)
def test_an_empty_or_malformed_check_is_rejected_at_load(check: dict[str, Any]) -> None:
    with pytest.raises(Exception):
        parse_node({"type": "card_tool_called", **check})
