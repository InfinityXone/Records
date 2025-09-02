"""Feedback aggregator and broadcast agent.

Echo is responsible for collecting feedback from users, system logs and
external sources to maintain emotional resonance and guide the
development of Infinity X One.  This worker reads from a
``feedback`` table in Supabase and broadcasts messages to other
agents via the handshake server or internal queues.  It also
maintains a simple sentiment analysis to adjust tone and
communication style.
"""

import datetime
from typing import List, Dict, Any

from ..supabase_utils import get_client, insert_log


def fetch_feedback() -> List[Dict[str, Any]]:
    """Fetch pending feedback entries from Supabase."""
    client = get_client()
    response = client.table("feedback").select("id, message, sentiment").eq("status", "pending").execute()
    return response.data or []


def broadcast(feedback: Dict[str, Any]) -> None:
    """Send a feedback message to other agents.

    This is a stub that could write to a message queue, post to
    WebSockets or insert into another table.  For now, it marks the
    feedback as processed.
    """
    client = get_client()
    client.table("feedback").update({"status": "processed"}).eq("id", feedback["id"]).execute()


def run() -> None:
    """Entry point for the echo feedback worker."""
    items = fetch_feedback()
    for item in items:
        broadcast(item)
    if items:
        insert_log(
            agent="EchoFeedback",
            message=f"Processed {len(items)} feedback messages",
            level="info",
        )


if __name__ == "__main__":
    run()