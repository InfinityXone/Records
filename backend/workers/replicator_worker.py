"""Replicator worker.

This worker is responsible for spawning additional copies of agents across
multiple nodes.  It reads a replication map from a JSON file (the
`agent_replicator.map.json` uploaded by the user) and writes replication
events into Supabase.  The actual replication logic (e.g. `kubectl scale`)
must be implemented by Codex or external orchestrators.  Here we simulate
replication by logging which agents would be deployed to which nodes.
"""

import json
import os
import time
from typing import Dict, List

from ..supabase_utils import fetch_pending_directives, insert_log, mark_directive_complete

AGENT_NAME = "Replicator"


def load_replicator_map() -> Dict[str, Dict[str, any]]:
    """Load the replication configuration from `agent_replicator.map.json`.

    The path can be overridden via the `REPLICATOR_MAP_PATH` environment variable.
    """
    path = os.getenv("REPLICATOR_MAP_PATH", os.path.join(os.getcwd(), "agent_replicator.map.json"))
    if not os.path.exists(path):
        # Fallback to the package file shipped with this deployment
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "agent_replicator.map.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "error_loading_map", "details": str(e)})
        return {}


def replicate_agent(name: str, config: Dict[str, any]) -> List[Dict[str, str]]:
    """Simulate replicating an agent to its target nodes.

    Returns a list of replication events for logging.
    """
    events = []
    targets = config.get("replicate_to", [])
    for node in targets:
        event = {"agent_name": name, "node": node, "status": "queued"}
        events.append(event)
        # In a real system you would call `kubectl` or the Kubernetes API here
    return events


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    payload = directive.get("payload", {})

    if command == "REPLICATE_SWARM":
        # Load map and replicate specified agents; if no agents provided, replicate all
        map_data = load_replicator_map()
        agents_to_replicate = payload.get("agents") or list(map_data.keys())
        all_events = []
        for agent_name in agents_to_replicate:
            cfg = map_data.get(agent_name)
            if not cfg:
                continue
            events = replicate_agent(agent_name, cfg)
            all_events.extend(events)
            # Log replication details
            for ev in events:
                insert_log("replication_events", {"agent": AGENT_NAME, **ev})
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "replication_executed", "details": all_events})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})

    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # Idle; replicator runs on demand
            time.sleep(600)


if __name__ == "__main__":
    run_worker()
