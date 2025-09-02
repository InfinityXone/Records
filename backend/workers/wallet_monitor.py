"""WalletMonitor worker.

This worker tracks the balances of the user’s crypto wallets and records
profits and airdrop receipts.  For security reasons it does not expose
private keys; instead it reads the addresses from environment variables.
In a full implementation you would integrate with a blockchain API
(Infura, Moralis, Alchemy, Solana RPC) to fetch live balances.  Here it
logs stubbed balances to Supabase.
"""

import os
import time
import random
from typing import Dict

from ..supabase_utils import fetch_pending_directives, insert_log, mark_directive_complete

AGENT_NAME = "WalletMonitor"


def get_wallet_addresses() -> Dict[str, str]:
    """Return the wallet addresses configured via environment variables."""
    return {
        "ethereum_primary": os.getenv("BASE_PUBLIC_WALLET_KEY", "0x0000"),
        "ethereum_secondary": os.getenv("ETHEREUM_ALTERNATE_WALLET_KEY", "0x0000"),
        "solana_primary": os.getenv("SOLANA_PRIVATE_WALLET_KEY", ""),
    }


def fetch_balances(addresses: Dict[str, str]) -> Dict[str, float]:
    """Simulate fetching wallet balances.

    Replace this stub with calls to a Web3 provider.  The return values
    here are random numbers for demonstration.
    """
    return {addr: round(random.uniform(0.0, 1.0), 4) for addr in addresses.values()}


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    addresses = get_wallet_addresses()
    if command == "CHECK_BALANCES":
        balances = fetch_balances(addresses)
        for addr, bal in balances.items():
            insert_log("wallet_balances", {"agent": AGENT_NAME, "address": addr, "balance": bal})
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "balances_fetched", "details": balances})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})
    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # By default, log balances daily
            addresses = get_wallet_addresses()
            balances = fetch_balances(addresses)
            for addr, bal in balances.items():
                insert_log("wallet_balances", {"agent": AGENT_NAME, "address": addr, "balance": bal})
            insert_log("agent_logs", {"agent": AGENT_NAME, "event": "heartbeat", "details": "logged wallet balances"})
            time.sleep(86400)  # once per day


if __name__ == "__main__":
    run_worker()
