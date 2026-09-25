"""Delegation hand-off: Planning Agent to Platform Agent to a Cluster Agent.

The check an author runs after deploying a change, minutes after the rollout
rather than hours later in the presubmit gate. It asks one read-only question
that must travel both delegation hops and scores the cards each hop filed.

Every card in the journey carries the portal session: a card a worker files
inherits its creator card's session. The tasks endpoint returns them with the
timestamps the interaction projection omits, but with no parent link, so a
Cluster Agent card is attributed to the platform card that was open when it
was filed.
"""

from __future__ import annotations

import urllib.parse
from datetime import UTC, datetime
from typing import Any

from cuj.utils.acceptance_criteria import AcceptanceCriteria, AcceptanceCriterion
from cuj.utils.interaction import projected_tasks, tool_operations
from cuj.utils.portal import CANONICAL_AGENT_ID, Portal
from cuj.utils.scenario import Scenario

# The prompt names no cluster. Given a name that appears in its roster, the
# Planning Agent routes straight to that Cluster Agent (agents/chat/SOUL.md
# §3) and the Platform Agent hop, the one this journey exists for, never runs.
PROMPT = """List the namespaces on the GKE cluster that kube-agents itself is \
installed on, and report that cluster's name and its namespace names. The \
Platform Agent must hand this to that cluster's Cluster Agent and wait for its \
answer rather than read the cluster itself. This is read-only: do not change \
anything."""

TIMEOUT_SECONDS = 300.0
PLATFORM_PROFILE = "platform"
CLUSTER_AGENT_PREFIX = "cluster-"

ACCEPTANCE_CRITERIA = (
    AcceptanceCriterion(
        "ac01-interaction-completed",
        "The conversation finishes successfully.",
        "terminal completed interaction",
    ),
    AcceptanceCriterion(
        "ac02-planning-agent-delegates",
        "The Planning Agent delegates instead of answering.",
        "root toolCalls contains a completed kanban_create",
    ),
    AcceptanceCriterion(
        "ac03-platform-card-done",
        "The Platform Agent's card runs and completes.",
        "a card assigned to platform is done after at least one run",
    ),
    AcceptanceCriterion(
        "ac04-cluster-card-filed",
        "The Platform Agent hands the question to a Cluster Agent.",
        "a cluster-* card was filed while a platform card was open",
    ),
    AcceptanceCriterion(
        "ac05-cluster-cards-done",
        "Every Cluster Agent card runs and completes.",
        "every handed-off cluster-* card is done after at least one run",
    ),
    AcceptanceCriterion(
        "ac06-platform-waited",
        "The Platform Agent completes its card only after the Cluster Agent "
        "answered, not on the dispatch receipt.",
        "each platform card completed at or after every cluster-* card filed "
        "while it was open",
    ),
)


def collect_handoff(portal: Portal, interaction: dict[str, Any]) -> dict[str, Any]:
    session_id = str(interaction.get("sessionId") or "")
    if not session_id:
        return {"handoff": {"sessionCards": []}}
    quoted = urllib.parse.quote(session_id, safe="")
    response = portal.get(f"agents/{CANONICAL_AGENT_ID}/sessions/{quoted}/tasks")
    cards = [card for card in response.get("tasks", []) if isinstance(card, dict)]
    return {"handoff": {"sessionCards": cards}}


def _timestamp(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _completed_at(card: dict[str, Any]) -> datetime | None:
    return _timestamp(card.get("updated_at")) if card.get("status") == "done" else None


def _filing_platform_card(
    card: dict[str, Any], platform_cards: list[dict[str, Any]]
) -> dict[str, Any] | None:
    # A card filed before any platform card, or after it completed, is the
    # Planning Agent's own and is not a hand-off.
    filed = _timestamp(card.get("created_at"))
    if filed is None:
        return None
    open_then = []
    for platform in platform_cards:
        opened = _timestamp(platform.get("created_at"))
        closed = _completed_at(platform)
        if opened is not None and opened <= filed and (closed is None or closed >= filed):
            open_then.append((opened, platform))
    return max(open_then, key=lambda pair: pair[0])[1] if open_then else None


def evaluate_acceptance(interaction: dict[str, Any]) -> AcceptanceCriteria:
    cards = (interaction.get("handoff") or {}).get("sessionCards") or []
    platform_cards = [card for card in cards if card.get("assignee") == PLATFORM_PROFILE]
    handed_off = []
    for card in cards:
        if not str(card.get("assignee") or "").startswith(CLUSTER_AGENT_PREFIX):
            continue
        platform = _filing_platform_card(card, platform_cards)
        if platform is not None:
            handed_off.append((card, platform))
    platform_tasks = projected_tasks(interaction, assignee=PLATFORM_PROFILE)
    completed_operations = tool_operations(interaction, completed_only=True)
    done_platform = [
        task
        for task in platform_tasks
        if task.get("status") == "done" and int(task.get("runCount") or 0) >= 1
    ]
    no_cluster_card = () if handed_off else ("no Cluster Agent card to score",)

    suite = AcceptanceCriteria(ACCEPTANCE_CRITERIA)
    suite.record(
        "ac01-interaction-completed",
        interaction.get("status") == "completed" and interaction.get("terminal") is True,
        {"status": interaction.get("status"), "error": interaction.get("error")},
    )
    suite.record(
        "ac02-planning-agent-delegates",
        "kanban_create" in completed_operations,
        completed_operations,
    )
    suite.record(
        "ac03-platform-card-done",
        bool(done_platform),
        [
            {key: task.get(key) for key in ("taskId", "status", "runCount", "error")}
            for task in platform_tasks
        ],
    )
    suite.record(
        "ac04-cluster-card-filed",
        bool(handed_off),
        [
            {key: card.get(key) for key in ("task_id", "assignee", "status", "created_at")}
            for card in cards
        ],
    )
    suite.record(
        "ac05-cluster-cards-done",
        bool(handed_off)
        and all(
            card.get("status") == "done" and int(card.get("run_count") or 0) >= 1
            for card, _ in handed_off
        ),
        [
            {
                key: card.get(key)
                for key in ("task_id", "assignee", "status", "run_count", "error")
            }
            for card, _ in handed_off
        ],
        blocked_by=no_cluster_card,
    )
    ordering = []
    for card, platform in handed_off:
        platform_done = _completed_at(platform)
        cluster_done = _completed_at(card)
        ordering.append(
            {
                "platformTaskId": platform.get("task_id"),
                "platformCompletedAt": platform_done and platform_done.isoformat(),
                "clusterTaskId": card.get("task_id"),
                "clusterCompletedAt": cluster_done and cluster_done.isoformat(),
                "waited": bool(
                    platform_done and cluster_done and platform_done >= cluster_done
                ),
            }
        )
    suite.record(
        "ac06-platform-waited",
        bool(ordering) and all(item["waited"] for item in ordering),
        ordering,
        blocked_by=no_cluster_card,
    )
    return suite


def build_prompt() -> str:
    return PROMPT


def test_01_handoff() -> None:
    Scenario(
        "delegation_handoff",
        build_prompt,
        evaluate_acceptance,
        collect_evidence=collect_handoff,
        default_timeout=TIMEOUT_SECONDS,
    ).run_test()
