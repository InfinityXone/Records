"""Resource Allocation Worker for Infinity X One.

This worker monitors operational metrics to determine if additional agents
should be spawned or scaled down.  It reads from the ``swarm_state`` and
``profit_ledger`` tables to assess system performance and writes
``agent_directives`` entries to instruct the replicator to scale the
swarm.  When profits are trending downward or the number of active
agents falls below a desired threshold, new replicas are requested.

The policy implemented here is intentionally simple.  In production,
replace the heuristics with a more sophisticated model based on
historical performance, resource usage and financial targets.
"""

import datetime
from ..supabase_utils import get_client


# Configuration constants.  Adjust these to tune scaling behaviour.
MIN_ACTIVE_AGENTS = 10  # Minimum number of active agents desired
MAX_ACTIVE_AGENTS = 200  # Cap to avoid runaway scaling
PROFIT_THRESHOLD = 10.0  # Minimum profit (USD) in the last 24h before scaling up


def main() -> None:
    client = get_client()

    # Fetch latest swarm state
    state_resp = (
        client.table("swarm_state")
        .select("active_agents, timestamp")
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )
    active_agents = None
    if state_resp.data:
        active_agents = state_resp.data[0].get("active_agents") or 0
    else:
        active_agents = 0

    # Calculate profit over the last 24 hours
    twenty_four_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    profits_resp = (
        client.table("profit_ledger")
        .select("amount, ts")
        .gte("ts", twenty_four_hours_ago.isoformat())
        .execute()
    )
    total_profit = 0.0
    for record in profits_resp.data or []:
        try:
            total_profit += float(record.get("amount", 0))
        except Exception:
            continue

    # Determine scaling action
    directives = []
    if (active_agents < MIN_ACTIVE_AGENTS) or (total_profit < PROFIT_THRESHOLD and active_agents < MAX_ACTIVE_AGENTS):
        # Scale up: request additional replicas for InfinityAgentOne
        directives.append({
            "agent": "Replicator",
            "command": "SCALE",
            "payload": {"target_agent": "InfinityAgentOne", "replicas": MIN_ACTIVE_AGENTS - active_agents + 1},
            "status": "pending",
            "timestamp": datetime.datetime.utcnow().timestamp(),
        })

    # If we exceed the maximum desired active agents and profits are high, scale down
    if active_agents > MAX_ACTIVE_AGENTS and total_profit > PROFIT_THRESHOLD * 5:
        directives.append({
            "agent": "Replicator",
            "command": "SCALE_DOWN",
            "payload": {"target_agent": "InfinityAgentOne", "replicas": active_agents - MAX_ACTIVE_AGENTS},
            "status": "pending",
            "timestamp": datetime.datetime.utcnow().timestamp(),
        })

    # Insert any directives into the database
    for directive in directives:
        client.table("agent_directives").insert(directive).execute()


if __name__ == "__main__":
    main()