"""FaucetHunter worker.

This worker is responsible for claiming rewards from a list of crypto
faucets and recording the outcomes in Supabase.  It periodically polls
Supabase for directives targeted at the agent name `FaucetHunter`.  When
a directive is received it executes the corresponding command.  If no
directives are pending, the worker performs its default behaviour: scan
the faucet list and log a heartbeat.

To customise the faucet list, edit the `FAUCETS` constant below or load
data from your `TOP_200_CRYPTO_FAUCETS_DATABASE.ts` module.  In this
skeleton the list contains only a handful of example entries.
"""

import os
import time
from typing import Dict, Any

from ..supabase_utils import fetch_pending_directives, insert_log, mark_directive_complete

AGENT_NAME = "FaucetHunter"

# A minimal set of faucet definitions.  Replace with the full list from
# `TOP_200_CRYPTO_FAUCETS_DATABASE.ts` or another source.
FAUCETS = [
    {"name": "solfaucet.com", "url": "https://solfaucet.com"},
    {"name": "ethdrop.io", "url": "https://ethdrop.io"},
    {"name": "matic‑rewards", "url": "https://maticrewards.com"},
]


def claim_faucet(faucet: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate claiming from a faucet.

    In a real implementation this function would perform HTTP requests,
    solve captchas and track claimed amounts.  Here it simply returns a
    stubbed success result.
    """
    # Simulate network latency
    time.sleep(0.5)
    return {
        "faucet": faucet["name"],
        "claimed": True,
        "amount": 0.001,  # placeholder value
        "token": "ETH",
    }


def process_directive(directive: Dict[str, Any]) -> None:
    """Execute a directive received from Supabase."""
    directive_id = directive["id"]
    command = directive["command"]
    payload = directive.get("payload", {})

    if command == "CLAIM_FAUCETS":
        results = []
        for faucet in FAUCETS:
            res = claim_faucet(faucet)
            results.append(res)
            insert_log("faucet_logs", {"agent": AGENT_NAME, **res})
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "claimed faucets", "details": results})

    elif command == "PING":
        # Simple heartbeat command
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "ping", "details": payload})

    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})

    # Mark directive as complete
    mark_directive_complete(directive_id)


def default_behaviour() -> None:
    """Run when no directives are pending.

    The default behaviour is to cycle through the faucet list and claim
    rewards quietly.  This ensures that the worker still earns crypto
    when it is not processing explicit commands.
    """
    for faucet in FAUCETS:
        res = claim_faucet(faucet)
        insert_log("faucet_logs", {"agent": AGENT_NAME, **res})
    insert_log("agent_logs", {"agent": AGENT_NAME, "event": "heartbeat", "details": "claimed default faucets"})


def run_worker() -> None:
    """Main polling loop for the FaucetHunter worker."""
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            # Process the first pending directive
            process_directive(directives[0])
        else:
            # Perform default behaviour
            default_behaviour()
        # Sleep briefly before polling again
        time.sleep(60)


if __name__ == "__main__":
    run_worker()
