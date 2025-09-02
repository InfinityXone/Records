"""Assign and manage wallets for agents.

This module wraps the wallet generator and provides an API to assign
new wallets to agents and retrieve the existing ledger.  When a
wallet is assigned, it is persisted to ``wallet_ledger.json`` along
with an ``assigned_to`` field storing the agent identifier.  The
ledger is kept in the root of the backend package.  In a real
deployment you would store this data in Supabase or a secure vault
instead of a local file.
"""

import json
import os
from pathlib import Path
from .generator import generate_wallet, save_wallet


def assign_wallet_to_agent(agent_id: str) -> dict:
    """Generate a wallet and associate it with a given agent.

    Parameters
    ----------
    agent_id:
        Unique identifier for the agent.  This can be the agent
        name or another identifier.  The ``assigned_to`` field will be
        recorded in the wallet entry.

    Returns
    -------
    dict
        The generated wallet with the added ``assigned_to`` field.
    """
    wallet = generate_wallet()
    wallet["assigned_to"] = agent_id
    save_wallet(wallet)
    return wallet


def load_wallets(filename: str = "wallet_ledger.json") -> list:
    """Load the current wallet ledger from disk.

    Parameters
    ----------
    filename:
        Name of the ledger file relative to the backend root.

    Returns
    -------
    list
        A list of wallet dictionaries.  If the file does not exist
        an empty list is returned.
    """
    ledger_path = Path(__file__).resolve().parent.parent / filename
    if not ledger_path.exists():
        return []
    try:
        with ledger_path.open("r") as f:
            return json.load(f)
    except Exception:
        return []