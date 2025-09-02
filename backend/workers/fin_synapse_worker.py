"""FinSynapse worker.

This worker manages yield farming, staking and reward distribution.  It
interfaces with the Infinity Coin smart contract (if deployed) and
monitors profits recorded in the `profit_ledger` table.  In this stub it
creates synthetic profit entries and logs reward events.  When the
Infinity Coin contract is available, update the `distribute_rewards`
function to call the contract and mint tokens.
"""

import random
import time
from typing import Dict

from ..supabase_utils import fetch_pending_directives, insert_log, mark_directive_complete, get_client

AGENT_NAME = "FinSynapse"


def simulate_profit_generation() -> Dict[str, float]:
    """Simulate earning profits across various wallets."""
    # Generate random profit amounts
    return {
        "eth": round(random.uniform(0.0, 0.01), 5),
        "sol": round(random.uniform(0.0, 0.02), 5),
        "base": round(random.uniform(0.0, 0.005), 5),
    }


def distribute_rewards(profits: Dict[str, float]) -> None:
    """Distribute rewards via Infinity Coin or log them.

    In a real deployment you would interact with the InfinityCoin smart
    contract using Web3.  Here we just log the reward events into
    Supabase.
    """
    total_reward = sum(profits.values()) * 1000  # convert to token units
    insert_log("reward_events", {"agent": AGENT_NAME, "reward": total_reward})


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    if command == "GENERATE_PROFITS":
        profits = simulate_profit_generation()
        insert_log("profit_ledger", {"agent": AGENT_NAME, **profits})
        distribute_rewards(profits)
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "generated_profits", "details": profits})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})
    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # Default: generate profits every hour
            profits = simulate_profit_generation()
            insert_log("profit_ledger", {"agent": AGENT_NAME, **profits})
            distribute_rewards(profits)
            insert_log("agent_logs", {"agent": AGENT_NAME, "event": "heartbeat", "details": "generated default profits"})
            time.sleep(3600)


if __name__ == "__main__":
    run_worker()
