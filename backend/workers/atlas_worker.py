"""Atlas worker.

This worker provisions compute resources for the swarm.  It requests free
or low‑cost instances from cloud providers and records node details in
Supabase (`compute_nodes` table).  Since the user has not provided actual
provider credentials, this module uses stubs.  You can extend the
`provision_node` function to integrate with AWS, GCP, Vast.ai or RunPod.
"""

import time
import random
from typing import Dict

from ..supabase_utils import fetch_pending_directives, insert_log, mark_directive_complete

AGENT_NAME = "Atlas"

# Example regions and dummy endpoints used for stub nodes
REGIONS = ["us-east-1", "us-west-2", "eu-central-1"]


def provision_node(region: str) -> Dict[str, str]:
    """Simulate provisioning a compute node in a region."""
    time.sleep(1)
    return {
        "region": region,
        "endpoint": f"https://{region}.dummy-provider.com/{random.randint(1000, 9999)}",
        "status": "active",
    }


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    payload = directive.get("payload", {})

    if command == "PROVISION_NODES":
        count = payload.get("count", 1)
        new_nodes = []
        for i in range(count):
            region = random.choice(REGIONS)
            node = provision_node(region)
            new_nodes.append(node)
            insert_log("compute_nodes", {"agent": AGENT_NAME, **node})
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "provisioned_nodes", "details": new_nodes})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})

    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # Idle until requested; Atlas is on‑demand
            time.sleep(300)


if __name__ == "__main__":
    run_worker()
