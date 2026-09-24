"""Delegation hand-off: Planning Agent to Platform Agent to a Cluster Agent.

The check an author runs after deploying a change, minutes after the rollout
rather than hours later in the presubmit gate. It asks one read-only question
that must travel both delegation hops and scores the cards each hop filed.

The interaction projection lists only the cards the Planning Agent filed, so
the Cluster Agent's card is found through the platform worker's session: the
dispatcher starts every worker with ``work kanban task <id>``, and a card the
worker files carries the worker's session id.
"""

from __future__ import annotations

import re
import urllib.parse
from datetime import UTC, datetime
from typing import Any

from cuj.utils.acceptance_criteria import AcceptanceCriteria, AcceptanceCriterion
from cuj.utils.interaction import projected_tasks, tool_operations
from cuj.utils.portal import CANONICAL_AGENT_ID, Portal
from cuj.utils.scenario import Scenario, required_env

PROMPT = """Have the Platform Agent ask the Cluster Agent for cluster \
{cluster} ({location}) in project {project_id} to list the namespaces on that \
cluster, then report the cluster name and the namespace names back to me. The \
Platform Agent must hand the question to that cluster's Cluster Agent and \
wait for its answer rather than read the cluster itself. This is read-only: \
do not change anything."""

TIMEOUT_SECONDS = 600.0
PLATFORM_PROFILE = "platform"
CLUSTER_AGENT_PREFIX = "cluster-"
SESSION_LISTING_LIMIT = 200
# The dispatcher's worker prompt, as admin_console/pages/chat.py matches it.
WORKER_PROMPT = re.compile(r"work\s+kanban(?:\s+task)?\s+([A-Za-z0-9_.:-]+)")

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
        "a root card assigned to platform is done after at least one run",
    ),
    AcceptanceCriterion(
        "ac04-cluster-card-filed",
        "The Platform Agent hands the question to a Cluster Agent.",
        "the platform worker's session filed at least one card assigned to a "
        "cluster-* profile",
    ),
    AcceptanceCriterion(
        "ac05-cluster-cards-done",
        "Every Cluster Agent card runs and completes.",
        "every cluster-* card is done after at least one run",
    ),
    AcceptanceCriterion(
        "ac06-platform-waited",
        "The Platform Agent completes its card only after the Cluster Agent "
        "answered, not on the dispatch receipt.",
        "each platform card completed at or after every cluster-* card its "
        "worker filed",
    ),
)


def _session_tasks(portal: Portal, session_id: str) -> list[dict[str, Any]]:
    quoted = urllib.parse.quote(session_id, safe="")
    response = portal.get(f"agents/{CANONICAL_AGENT_ID}/sessions/{quoted}/tasks")
    return [card for card in response.get("tasks", []) if isinstance(card, dict)]


def collect_handoff(portal: Portal, interaction: dict[str, Any]) -> dict[str, Any]:
    root_session = str(interaction.get("sessionId") or "")
    root_cards = _session_tasks(portal, root_session) if root_session else []
    platform_ids = {
        str(card.get("task_id"))
        for card in root_cards
        if card.get("assignee") == PLATFORM_PROFILE
    }
    query = urllib.parse.urlencode(
        {
            "cutoff": str(interaction.get("createdAt") or ""),
            "limit": SESSION_LISTING_LIMIT,
        }
    )
    listing = portal.get(f"agents/{CANONICAL_AGENT_ID}/sessions?{query}")
    workers = []
    for conversation in listing.get("conversations", []):
        if not isinstance(conversation, dict):
            continue
        if conversation.get("profile") != PLATFORM_PROFILE:
            continue
        match = WORKER_PROMPT.search(str(conversation.get("preview") or ""))
        if match and match.group(1) in platform_ids:
            workers.append(
                {
                    "sessionId": str(conversation.get("session_id") or ""),
                    "taskId": match.group(1),
                }
            )
    cluster_cards = [
        {**card, "workerTaskId": worker["taskId"]}
        for worker in workers
        for card in _session_tasks(portal, worker["sessionId"])
        if str(card.get("assignee") or "").startswith(CLUSTER_AGENT_PREFIX)
    ]
    return {
        "handoff": {
            "rootCards": root_cards,
            "workerSessions": workers,
            "clusterCards": cluster_cards,
            "sessionListingTruncated": bool(listing.get("truncated")),
        }
    }


def _timestamp(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def evaluate_acceptance(interaction: dict[str, Any]) -> AcceptanceCriteria:
    handoff = interaction.get("handoff") or {}
    root_cards = handoff.get("rootCards") or []
    workers = handoff.get("workerSessions") or []
    cluster_cards = handoff.get("clusterCards") or []
    platform_tasks = projected_tasks(interaction, assignee=PLATFORM_PROFILE)
    completed_operations = tool_operations(interaction, completed_only=True)
    done_platform = [
        task
        for task in platform_tasks
        if task.get("status") == "done" and int(task.get("runCount") or 0) >= 1
    ]
    listing_blocker = (
        ("session listing was truncated; a worker session may be missing",)
        if handoff.get("sessionListingTruncated")
        else ()
    )
    no_cluster_card = () if cluster_cards else ("no Cluster Agent card to score",)

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
        bool(cluster_cards),
        {
            "workerSessions": workers,
            "clusterCards": [
                {key: card.get(key) for key in ("task_id", "assignee", "status")}
                for card in cluster_cards
            ],
        },
        blocked_by=() if cluster_cards else listing_blocker,
    )
    suite.record(
        "ac05-cluster-cards-done",
        bool(cluster_cards)
        and all(
            card.get("status") == "done" and int(card.get("run_count") or 0) >= 1
            for card in cluster_cards
        ),
        [
            {
                key: card.get(key)
                for key in ("task_id", "assignee", "status", "run_count", "error")
            }
            for card in cluster_cards
        ],
        blocked_by=no_cluster_card,
    )
    completed_at = {
        str(card.get("task_id")): _timestamp(card.get("updated_at"))
        for card in root_cards
        if card.get("status") == "done"
    }
    ordering = []
    for card in cluster_cards:
        platform_done = completed_at.get(str(card.get("workerTaskId")))
        cluster_done = (
            _timestamp(card.get("updated_at"))
            if card.get("status") == "done"
            else None
        )
        ordering.append(
            {
                "platformTaskId": card.get("workerTaskId"),
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
    return PROMPT.format(
        cluster=required_env("CUJ_CLUSTER_NAME"),
        location=required_env("CUJ_CLUSTER_LOCATION"),
        project_id=required_env("CUJ_PROJECT_ID"),
    )


def test_01_handoff() -> None:
    Scenario(
        "delegation_handoff",
        build_prompt,
        evaluate_acceptance,
        collect_evidence=collect_handoff,
        default_timeout=TIMEOUT_SECONDS,
    ).run_test()
