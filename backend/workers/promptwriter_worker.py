"""PromptWriter worker.

This worker acts as the meta‑architect and orchestrator for the swarm.  It
listens for high‑level directives (e.g. INITIATE_PROTOCOL) and fans them
out to other agents by creating new directives.  It also manages
periodic tasks such as writing memory checkpoints or scaling the swarm.
"""

import time
from typing import Dict, Any

from ..supabase_utils import (
    fetch_pending_directives,
    insert_log,
    mark_directive_complete,
    get_client,
)

AGENT_NAME = "PromptWriter"


def dispatch_directive(agent: str, command: str, payload: Dict[str, Any]) -> None:
    """Create a new directive for another agent."""
    client = get_client()
    data = {
        "agent": agent,
        "command": command,
        "payload": payload,
        "status": "pending",
        "timestamp": time.time(),
    }
    client.table("agent_directives").insert(data).execute()


def process_initiate_protocol(payload: Dict[str, Any]) -> None:
    """Handle the INITIATE_PROTOCOL directive.

    This function fans out tasks to various workers based on the doctrines
    and layers provided.  For example, it may instruct the Replicator
    worker to scale out the swarm or the KeyHarvester to harvest keys.
    """
    doctrines = payload.get("doctrines", [])
    agents = payload.get("agents", [])
    layers = payload.get("layers", [])

    # Log that the protocol has been received
    insert_log(
        "agent_logs",
        {
            "agent": AGENT_NAME,
            "event": "initiate_protocol_received",
            "details": {
                "doctrines": doctrines,
                "agents": agents,
                "layers": layers,
            },
        },
    )

    # Example: if Omega is in doctrines, start a replication of the swarm
    if "Omega Unified Unlock" in doctrines or "Infinity Alpha Prime Protocol" in doctrines:
        dispatch_directive("Replicator", "REPLICATE_SWARM", {"agents": agents})

    # Always kick off a key harvest and compute provisioning at protocol start
    dispatch_directive("KeyHarvester", "HARVEST_KEYS", {})
    dispatch_directive("Atlas", "PROVISION_NODES", {"count": max(1, len(agents))})
    dispatch_directive("FaucetHunter", "CLAIM_FAUCETS", {})
    dispatch_directive("FinSynapse", "GENERATE_PROFITS", {})
    dispatch_directive("Guardian", "RUN_AUDIT", {})
    dispatch_directive("PickyBot", "ANALYSE_PERFORMANCE", {})


def process_directive(directive: Dict[str, Any]) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    payload = directive.get("payload", {})
    if command == "INITIATE_PROTOCOL":
        process_initiate_protocol(payload)
    else:
        insert_log(
            "agent_logs",
            {"agent": AGENT_NAME, "event": "unknown_directive", "details": command},
        )
    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # PromptWriter can perform maintenance tasks here, such as
            # persisting memory or generating daily status reports.  For
            # simplicity we just sleep.
            time.sleep(120)


if __name__ == "__main__":
    run_worker()
