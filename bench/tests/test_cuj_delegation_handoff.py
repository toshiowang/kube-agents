"""Offline tests for the delegation hand-off journey's collector and criteria.

The records below are what the portal API returned on a live install
(platform-agent-host, 2026-09-25) for the journey's session, trimmed to the
fields the journey reads. The platform card filed both Cluster Agent cards as
its children and completed at 01:33:11, before either of them ran.
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

SESSION = "portal_delegation_handoff_77affa265cbb43e3a28a990e1c4cef1c"
CLUSTER_AGENT = "cluster-toshiowang-gkedemos-platform-agent-host-us-east4"
PLATFORM_CARD = {
    "task_id": "t_21165c27",
    "assignee": "platform",
    "status": "done",
    "run_count": 2,
    "created_at": "2026-09-25T01:32:12Z",
    "updated_at": "2026-09-25T01:33:11Z",
}
CLUSTER_CARDS = [
    {
        "task_id": "t_17eab87a",
        "assignee": CLUSTER_AGENT,
        "status": "done",
        "run_count": 1,
        "created_at": "2026-09-25T01:32:52Z",
        "updated_at": "2026-09-25T01:33:37Z",
    },
    {
        "task_id": "t_04d3641e",
        "assignee": CLUSTER_AGENT,
        "status": "done",
        "run_count": 1,
        "created_at": "2026-09-25T01:33:03Z",
        "updated_at": "2026-09-25T01:33:39Z",
    },
]
WAITED_PLATFORM_CARD = {**PLATFORM_CARD, "updated_at": "2026-09-25T01:33:45Z"}


class FakePortal:
    def __init__(self, cards: list[dict]) -> None:
        self.cards = cards
        self.paths: list[str] = []

    def get(self, path: str) -> dict:
        self.paths.append(path)
        return {"tasks": self.cards, "truncated": False}


def _interaction(platform_card: dict, cluster_cards: list[dict]) -> dict:
    interaction = {
        "sessionId": SESSION,
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
    portal = FakePortal([platform_card, *cluster_cards])
    return {**interaction, **collect_handoff(portal, interaction)}


def _results(interaction: dict) -> dict[str, bool]:
    return {
        result.criterion.id: result.passed
        for result in evaluate_acceptance(interaction).results
    }


def test_collector_reads_the_journeys_session():
    portal = FakePortal([PLATFORM_CARD, *CLUSTER_CARDS])

    handoff = collect_handoff(portal, {"sessionId": SESSION})["handoff"]

    assert portal.paths == [f"agents/platform-agent/sessions/{SESSION}/tasks"]
    assert [card["task_id"] for card in handoff["sessionCards"]] == [
        "t_21165c27",
        "t_17eab87a",
        "t_04d3641e",
    ]


def test_platform_card_completed_before_its_cluster_cards_fails_only_the_wait():
    results = _results(_interaction(PLATFORM_CARD, CLUSTER_CARDS))

    assert results.pop("ac06-platform-waited") is False
    assert all(results.values()), results


def test_platform_card_completed_after_every_cluster_card_passes():
    assert all(_results(_interaction(WAITED_PLATFORM_CARD, CLUSTER_CARDS)).values())


def test_a_cluster_card_still_running_fails_the_journey():
    running = [CLUSTER_CARDS[0], {**CLUSTER_CARDS[1], "status": "running"}]

    results = _results(_interaction(WAITED_PLATFORM_CARD, running))

    assert results["ac05-cluster-cards-done"] is False
    assert results["ac06-platform-waited"] is False


def test_platform_agent_answering_itself_fails_the_hand_off():
    results = _results(_interaction(PLATFORM_CARD, []))

    assert results["ac03-platform-card-done"] is True
    assert results["ac04-cluster-card-filed"] is False
    assert results["ac05-cluster-cards-done"] is False
    assert results["ac06-platform-waited"] is False


def test_a_cluster_card_filed_outside_the_platform_cards_run_is_not_a_hand_off():
    before = {**CLUSTER_CARDS[0], "created_at": "2026-09-25T01:32:10Z"}
    after = {**CLUSTER_CARDS[1], "created_at": "2026-09-25T01:33:50Z"}

    results = _results(_interaction(WAITED_PLATFORM_CARD, [before, after]))

    assert results["ac04-cluster-card-filed"] is False
