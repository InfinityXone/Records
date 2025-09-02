"""Wallet rotation worker for Infinity X One.

This worker ensures that each active agent has a dedicated wallet.  It
periodically reads the swarm state to determine how many agents are
active and assigns new wallets via the local ``wallet`` package when
necessary.  In a real deployment you should replace this logic with
calls to a secure key management service and update the agent records
in Supabase to reflect the new wallet assignments.
"""

import time
import os
from ..supabase_utils import get_client
from ..wallet.manager import assign_wallet_to_agent, load_wallets

def run_once() -> None:
    """Execute a single wallet rotation pass.

    The function reads the most recent ``swarm_state`` record to
    determine the number of active agents.  If there are more agents
    than wallets currently assigned, new wallets will be generated
    and assigned sequentially.  This prevents multiple agents from
    sharing a single private key.
    """
    client = get_client()
    # Fetch the latest swarm_state entry
    resp = (
        client.table("swarm_state")
        .select("active_agents")
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )
    active_count = None
    if resp.data:
        entry = resp.data[0]
        active_count = entry.get("active_agents")
    if not active_count or active_count <= 0:
        return
    # Determine how many wallets are already present
    ledger = load_wallets()
    existing_count = len(ledger)
    # Assign missing wallets
    for i in range(existing_count, active_count):
        agent_id = f"agent_{i+1}"
        assign_wallet_to_agent(agent_id)
        print(f"[wallet_rotator] Assigned new wallet to {agent_id}")


def main() -> None:
    """Run the wallet rotator in a loop.

    The worker sleeps for a configurable interval (default 1 hour)
    between rotation passes.  This allows it to run as a long‑lived
    deployment rather than a CronJob.  When used in a CronJob,
    simply invoke ``run_once()`` instead of entering an infinite loop.
    """
    interval_seconds = int(os.getenv("WALLET_ROTATOR_INTERVAL", "3600"))
    while True:
        try:
            run_once()
        except Exception as exc:
            print(f"[wallet_rotator] Error during wallet rotation: {exc}")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_once()