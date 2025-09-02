"""KeyHarvester worker.

This worker searches for free API keys, trial accounts and other resources
that can be used by the swarm.  It writes harvested credentials into
Supabase tables such as `api_keys` and triggers notifications for other
agents.  In this stub implementation it simply simulates harvesting a
Moralis, Infura and Alchemy API key.
"""

import time
from typing import Dict

from ..supabase_utils import fetch_pending_directives, insert_log, mark_directive_complete

AGENT_NAME = "KeyHarvester"


def harvest_keys() -> Dict[str, str]:
    """Simulate harvesting API keys from popular providers."""
    # In reality this would involve creating accounts or scraping public trials.
    time.sleep(1)
    return {
        "moralis": "stubbed‑moralis‑key",
        "infura": "stubbed‑infura‑key",
        "alchemy": "stubbed‑alchemy‑key",
    }


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]

    if command == "HARVEST_KEYS":
        keys = harvest_keys()
        # Insert each key into an `api_keys` table.  The table should be created
        # in Supabase with columns: provider, key, ts
        for provider, key in keys.items():
            insert_log("api_keys", {"provider": provider, "key": key, "agent": AGENT_NAME})
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "harvested_keys", "details": keys})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})

    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # In absence of directives, harvest keys periodically
            keys = harvest_keys()
            for provider, key in keys.items():
                insert_log("api_keys", {"provider": provider, "key": key, "agent": AGENT_NAME})
            insert_log("agent_logs", {"agent": AGENT_NAME, "event": "heartbeat", "details": "harvested default keys"})
        time.sleep(1800)  # run every 30 minutes


if __name__ == "__main__":
    run_worker()
