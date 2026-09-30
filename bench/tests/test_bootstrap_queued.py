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

"""The queue read, the ``bootstrap_queued`` verifier and the stack's queue cleanup.

The queue under test is a real findings store: ``inventory_findings.py
extract`` runs on the raw report the bootstrap-ranking stack plants, and its
items go through ``register_scored`` into ``findings_queue``'s own schema, the
path the ``register_inventory_scores`` tool takes. Only the scores are written
here, since the model writes them on the install.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sqlite3
import subprocess
import sys
import textwrap
import tomllib
from pathlib import Path
from typing import Any

import pytest
import yaml
from devops_bench.verification.base import VERIFIERS
from devops_bench.verification.spec import parse_node

from kube_agents_bench import onboarding
from kube_agents_bench.verifiers import BootstrapQueuedVerifier

REPO = Path(__file__).resolve().parents[2]
STACK = REPO / "bench" / "tf" / "prebuilt" / "bootstrap-ranking"
RAW = STACK / "inventory-raw.txt"
SCRIPTS = REPO / "agents" / "platform" / "scripts"
EXTRACT = SCRIPTS / "inventory_findings.py"
TASK = REPO / "bench" / "tasks" / "bootstrap-inventory-ranking-delivery" / "task.yaml"

RUBRIC = {"B": 3, "L": 6, "detect": 3, "recover": 2, "C": 1.0}
SCORE = {
    "rubric": RUBRIC,
    "recommendation": {"action": "fix it", "rationale": "risk", "risk": "outage"},
    "remediation": {"kind": "manifest", "path": "k8s/app.yaml", "note": "edit"},
    "verification": {"kind": "kubectl", "command": "kubectl get deploy", "still_failing_when": "empty"},
}

# inventory_findings imports findings_queue as a sibling. Appended, not
# inserted, so the path cannot shadow a same-named module later in the session.
sys.path.append(str(SCRIPTS))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fq = _load("findings_queue", SCRIPTS / "findings_queue.py")
inv = _load("inventory_findings", EXTRACT)


def _spec() -> list[dict[str, Any]]:
    return yaml.safe_load(TASK.read_text().split("\n---\n", 1)[1])["verification_spec"]


def _objective(name: str = "findings-queued") -> dict[str, Any]:
    return next(e for e in _spec() if e["name"] == name)["check"]


def _extract(out: Path) -> dict[str, Any]:
    subprocess.run(
        [sys.executable, str(EXTRACT), "extract", "--raw", str(RAW), "--out", str(out)],
        check=True,
        capture_output=True,
    )
    return json.loads(out.read_text())


def _register(db: Path, items: dict[str, Any], *, source: str | None = None, project: str | None = None) -> None:
    """Registers ``items`` the way the tool does, optionally relabelled.

    A finding's identity leaves out its source, so a relabelled source also
    renames the object: the same identity would overwrite the inventory row.
    """
    scores = {"scores": {i["id"]: SCORE for i in items["items"]}}
    with sqlite3.connect(db) as conn:
        fq.init_findings_schema(conn)

        def post(batch: list[dict], scope: dict | None) -> dict:
            if source:
                batch = [dict(p, source=source, object=f"{p['object']}-{source}") for p in batch]
            if project:
                batch = [dict(p, project=project) for p in batch]
            return fq.register_findings(conn, batch, scope)

        inv.register_scored(items, scores, "INVENTORY.items.json", post, lambda line: None)


def _rows(db: Path) -> list[tuple[str, str, str]]:
    with sqlite3.connect(db) as conn:
        return sorted(conn.execute("SELECT source, project, check_slug FROM findings"))


def _local_shell(script: str, timeout: float) -> str:
    return subprocess.run(["sh", "-c", script], capture_output=True, text=True, timeout=timeout, check=True).stdout


@pytest.fixture
def queue(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The store the read command opens, with the command run locally."""
    db = tmp_path / "session_kv.db"
    monkeypatch.setattr(onboarding, "QUEUE_DB", str(db))
    monkeypatch.setattr(onboarding, "AGENT_PYTHON", sys.executable)
    monkeypatch.setattr(onboarding, "agent_shell", _local_shell)
    monkeypatch.delenv(onboarding.QUEUE_DB_ENV, raising=False)
    return db


@pytest.fixture
def items(tmp_path: Path) -> dict[str, Any]:
    return _extract(tmp_path / "INVENTORY.items.json")


def _verify(timeout: float = 0.0, **overrides: Any):
    check = {**_objective(), **overrides}
    return BootstrapQueuedVerifier(**check).verify(timeout)


# --- the case and its fixture ---------------------------------------------


def test_the_case_expects_what_extract_writes_from_the_planted_report(items: dict[str, Any]) -> None:
    check = _objective()
    assert {i["project"] for i in items["items"]} == {check["project"]}
    assert sorted((i["check"], i["object"]) for i in items["items"]) == sorted(
        (e["check"], e["object"]) for e in check["expected_findings"]
    )


def test_the_queue_check_and_the_items_check_expect_the_same_pairs() -> None:
    assert _objective()["expected_findings"] == _objective("findings-extracted")["expected_findings"]


def test_the_stack_clears_the_project_the_case_reads() -> None:
    main_tf = (STACK / "main.tf").read_text()
    assert f'queue_project = "{_objective()["project"]}"' in main_tf


def test_the_reader_names_the_store_and_source_the_platform_does() -> None:
    server = (SCRIPTS / "session_kv_server.py").read_text()
    assert f'"{onboarding.QUEUE_DB_ENV}"' in server
    assert onboarding.QUEUE_DB in server
    assert inv.SOURCE == onboarding.INVENTORY_SOURCE


# --- the read -------------------------------------------------------------


def test_the_read_returns_the_registered_rows(queue: Path, items: dict[str, Any]) -> None:
    _register(queue, items)
    rows, why = onboarding.read_queue(onboarding.agent_shell, "onboarding-demo-prod", 5.0)
    assert why == ""
    assert sorted((r["check"], r["object"]) for r in rows) == sorted((i["check"], i["object"]) for i in items["items"])
    assert {r["cluster"] for r in rows} == {"prod-east"}


def test_the_read_skips_other_sources_and_projects(queue: Path, items: dict[str, Any]) -> None:
    _register(queue, items, source="audit")
    _register(queue, items, project="elsewhere")
    rows, why = onboarding.read_queue(onboarding.agent_shell, "onboarding-demo-prod", 5.0)
    assert (rows, why) == ([], "")


def test_the_read_follows_the_env_override(queue: Path, items: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    other = tmp_path / "other.db"
    _register(other, items)
    monkeypatch.setenv(onboarding.QUEUE_DB_ENV, str(other))
    rows, _ = onboarding.read_queue(onboarding.agent_shell, "onboarding-demo-prod", 5.0)
    assert len(rows) == len(items["items"])


def test_no_store_is_an_error_naming_it(queue: Path) -> None:
    rows, why = onboarding.read_queue(onboarding.agent_shell, "onboarding-demo-prod", 5.0)
    assert rows is None
    assert str(queue) in why


def test_a_store_without_the_table_is_an_error(queue: Path) -> None:
    sqlite3.connect(queue).close()
    rows, why = onboarding.read_queue(onboarding.agent_shell, "onboarding-demo-prod", 5.0)
    assert rows is None
    assert "no such table" in why


def test_a_failed_exec_is_a_failed_read() -> None:
    rows, why = onboarding.read_queue(lambda s, t: "", "p", 5.0)
    assert rows is None
    assert "could not be read" in why


@pytest.mark.parametrize(
    "body,expected",
    [("not json", "did not return JSON"), ("[]", "other than an object"), ('{"rows": "x"}', "no list of rows")],
)
def test_a_malformed_reply_is_a_failed_read(body: str, expected: str) -> None:
    rows, why = onboarding.read_queue(lambda s, t: f"{onboarding.QUEUE_READ}\n{body}", "p", 5.0)
    assert rows is None
    assert expected in why


# --- the objective --------------------------------------------------------


def test_the_registered_findings_pass(queue: Path, items: dict[str, Any]) -> None:
    _register(queue, items)
    result = _verify()
    assert result.status == "pass", result.reason
    assert "the 6 expected finding(s)" in result.reason


def test_nothing_registered_fails(queue: Path, items: dict[str, Any]) -> None:
    _register(queue, items, project="elsewhere")
    result = _verify()
    assert result.status == "fail"
    assert "the stage registered nothing" in result.reason


def test_a_missing_finding_is_named(queue: Path, items: dict[str, Any]) -> None:
    items["items"] = [i for i in items["items"] if i["object"] != "cart"]
    _register(queue, items)
    result = _verify()
    assert result.status == "fail"
    assert "missing [('probes-readiness', 'cart')]" in result.reason


def test_a_finding_the_report_does_not_carry_is_named(queue: Path, items: dict[str, Any]) -> None:
    _register(queue, items)
    result = _verify(expected_findings=_objective()["expected_findings"][1:])
    assert result.status == "fail"
    assert "not in the raw report's block [('sa-key-in-secret', 'checkout')]" in result.reason


def test_an_unreadable_store_is_an_error(queue: Path) -> None:
    assert _verify().status == "error"


# --- the stack's cleanup --------------------------------------------------


def _stack_queue_script() -> str:
    main_tf = (STACK / "main.tf").read_text()
    project = re.search(r'queue_project = "([^"]+)"', main_tf).group(1)
    body = re.search(r"queue_py\s*=\s*<<-EOP\n(.*?)\n\s*EOP\n", main_tf, re.S).group(1)
    return textwrap.dedent(body).replace("${local.queue_project}", project)


def _run_cleanup(db: Path) -> str:
    return subprocess.run(
        [sys.executable, "-c", _stack_queue_script()],
        env={"SESSION_KV_DB_PATH": str(db)},
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def test_the_cleanup_deletes_only_the_projects_inventory_rows(tmp_path: Path, items: dict[str, Any]) -> None:
    db = tmp_path / "session_kv.db"
    _register(db, items)
    _register(db, items, source="audit")
    _register(db, items, project="elsewhere")
    out = _run_cleanup(db)
    assert f"deleted {len(items['items'])} queued finding(s) for onboarding-demo-prod" in out
    left = _rows(db)
    assert {(s, p) for s, p, _ in left} == {("audit", "onboarding-demo-prod"), ("inventory", "elsewhere")}
    assert len(left) == 2 * len(items["items"])


@pytest.mark.parametrize("make_table", [False, True])
def test_the_cleanup_passes_on_a_store_that_holds_nothing(tmp_path: Path, make_table: bool) -> None:
    db = tmp_path / "session_kv.db"
    if make_table:
        sqlite3.connect(db).close()
    out = _run_cleanup(db)
    assert ("no findings table" if make_table else "no findings queue") in out


# --- registration ---------------------------------------------------------


def test_the_verifier_is_published_as_an_entry_point() -> None:
    with (REPO / "bench" / "pyproject.toml").open("rb") as fh:
        eps = tomllib.load(fh)["project"]["entry-points"]["devops_bench.verifiers"]
    assert eps["bootstrap_queued"] == "kube_agents_bench.verifiers:BootstrapQueuedVerifier"


def test_parse_node_builds_the_case_objective() -> None:
    assert isinstance(parse_node(_objective()), BootstrapQueuedVerifier)
    assert VERIFIERS.get("bootstrap_queued") is BootstrapQueuedVerifier


@pytest.mark.parametrize(
    "check",
    [
        {"project": "", "expected_findings": [{"check": "c", "object": "o"}]},
        {"project": "p", "expected_findings": []},
        {"expected_findings": [{"check": "c", "object": "o"}]},
    ],
)
def test_an_empty_or_malformed_check_is_rejected_at_load(check: dict[str, Any]) -> None:
    with pytest.raises(Exception):
        parse_node({"type": "bootstrap_queued", **check})
