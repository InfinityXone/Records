"""Guardian worker.

This worker enforces the oath and integrity rules of the Infinity X One
swarm.  It periodically scans the `agent_logs` table for anomalies,
missing heartbeats or ethical violations and writes audit events to
`integrity_events`.  In this stub it randomly flags logs as audits.
"""

import random
import time
from typing import Dict

from ..supabase_utils import get_client, insert_log, fetch_pending_directives, mark_directive_complete

AGENT_NAME = "Guardian"


def audit_logs() -> None:
    """Perform a random audit on recent agent logs."""
    client = get_client()
    resp = client.table("agent_logs").select("id, agent, event, ts").order("ts", desc=True).limit(10).execute()
    logs = resp.data or []
    if not logs:
        return
    # Randomly pick a log and write an audit event
    log_entry = random.choice(logs)
    insert_log(
        "integrity_events",
        {
            "agent": AGENT_NAME,
            "checked_agent": log_entry["agent"],
            "log_id": log_entry["id"],
            "status": "ok",
        },
    )


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    if command == "RUN_AUDIT":
        audit_logs()
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "run_audit", "details": "completed"})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})
    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # Perform audits every hour
            audit_logs()
            insert_log("agent_logs", {"agent": AGENT_NAME, "event": "heartbeat", "details": "audit check"})
            time.sleep(3600)


if __name__ == "__main__":
    run_worker()
