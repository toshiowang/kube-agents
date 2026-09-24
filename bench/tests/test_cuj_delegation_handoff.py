"""Offline tests for the delegation hand-off journey's collector and criteria.

The records below are what the portal API returned on a live install
(platform-agent-host, 2026-09-24) for a platform card that fanned out to four
Cluster Agents, trimmed to the fields the journey reads. The platform card
completed at 19:51:15, one second before its last Cluster Agent card; the
task_events ids on the install put the two completions in that order.
"""

from __future__ import annotations

import sys
from pathlib import Path

BENCH_ROOT = Path(__file__).resolve().parents[1]
if str(BENCH_ROOT) not in sys.path:
    sys.path.insert(0, str(BENCH_ROOT))

from cuj.delegation.test_01_handoff import (  # noqa: E402
    collect_handoff,
    evaluate_acceptance,
)

ROOT_SESSION = "portal_delegation_handoff_0"
WORKER_SESSION = "20260924_194813_cf3581"
PLATFORM_CARD = {
    "task_id": "t_9d83bd90",
    "assignee": "platform",
    "status": "done",
    "run_count": 1,
    "updated_at": "2026-09-24T19:51:15Z",
}
CLUSTER_CARDS = [
    {
        "task_id": "t_43e2663b",
        "assignee": "cluster-toshiowang-gkedemos-platform-agent-host-us-east4",
        "status": "done",
        "run_count": 1,
        "updated_at": "2026-09-24T19:50:39Z",
    },
    {
        "task_id": "t_5694040e",
        "assignee": "cluster-toshiowang-gkedemos-support-eval-cluster-us-central1-a",
        "status": "done",
        "run_count": 1,
        "updated_at": "2026-09-24T19:51:16Z",
    },
]
CONVERSATIONS = [
    {
        "session_id": WORKER_SESSION,
        "profile": "platform",
        "preview": "work kanban task t_9d83bd90",
    },
    {
        "session_id": "20260924_194410_b97100",
        "profile": "platform",
        "preview": "work kanban task t_3ce8f00f",
    },
    {"session_id": ROOT_SESSION, "profile": "default", "preview": "Have the"},
]


class FakePortal:
    def __init__(self, tasks: dict[str, list[dict]]) -> None:
        self.tasks = tasks
        self.paths: list[str] = []

    def get(self, path: str) -> dict:
        self.paths.append(path)
        if "/sessions?" in path:
            return {"conversations": CONVERSATIONS, "truncated": False}
        session = path.split("/sessions/")[1].removesuffix("/tasks")
        return {"tasks": self.tasks.get(session, []), "truncated": False}


def _interaction(platform_card: dict, cluster_cards: list[dict]) -> dict:
    interaction = {
        "sessionId": ROOT_SESSION,
        "createdAt": "2026-09-24T19:48:00+00:00",
        "status": "completed",
        "terminal": True,
        "toolCalls": [{"name": "kanban_create", "status": "completed"}],
        "tasks": [
            {
                "taskId": platform_card["task_id"],
                "assignee": "platform",
                "status": platform_card["status"],
                "runCount": platform_card["run_count"],
            }
        ],
    }
    portal = FakePortal({ROOT_SESSION: [platform_card], WORKER_SESSION: cluster_cards})
    return {**interaction, **collect_handoff(portal, interaction)}


def _results(interaction: dict) -> dict[str, bool]:
    return {
        result.criterion.id: result.passed
        for result in evaluate_acceptance(interaction).results
    }


def test_cluster_cards_are_found_through_the_platform_workers_session():
    handoff = _interaction(PLATFORM_CARD, CLUSTER_CARDS)["handoff"]

    assert handoff["workerSessions"] == [
        {"sessionId": WORKER_SESSION, "taskId": "t_9d83bd90"}
    ]
    assert [card["task_id"] for card in handoff["clusterCards"]] == [
        "t_43e2663b",
        "t_5694040e",
    ]


def test_platform_card_completed_before_its_cluster_card_fails_only_the_wait():
    results = _results(_interaction(PLATFORM_CARD, CLUSTER_CARDS))

    assert results.pop("ac06-platform-waited") is False
    assert all(results.values()), results


def test_platform_card_completed_after_every_cluster_card_passes():
    platform_card = {**PLATFORM_CARD, "updated_at": "2026-09-24T19:51:16Z"}

    assert all(_results(_interaction(platform_card, CLUSTER_CARDS)).values())


def test_a_cluster_card_still_running_fails_the_journey():
    running = [CLUSTER_CARDS[0], {**CLUSTER_CARDS[1], "status": "running"}]
    platform_card = {**PLATFORM_CARD, "updated_at": "2026-09-24T19:52:00Z"}

    results = _results(_interaction(platform_card, running))

    assert results["ac05-cluster-cards-done"] is False
    assert results["ac06-platform-waited"] is False


def test_platform_agent_answering_itself_fails_the_hand_off():
    results = _results(_interaction(PLATFORM_CARD, []))

    assert results["ac03-platform-card-done"] is True
    assert results["ac04-cluster-card-filed"] is False
    assert results["ac05-cluster-cards-done"] is False
    assert results["ac06-platform-waited"] is False
