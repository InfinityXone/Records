"""Basic wallet generator for Infinity X One.

This module exposes two functions:

* ``generate_wallet()`` – returns a dictionary with a random
  hexadecimal address and private key.  The values are placeholders
  suitable for development and do not correspond to a real blockchain.

* ``save_wallet(wallet, filename="wallet_ledger.json")`` – appends
  the wallet to a JSON ledger on disk.  If the file does not exist
  it will be created.  In production you should never persist
  private keys in plain text; instead use a vault or secure
  secret store.
"""

import json
import os
import secrets
from pathlib import Path

def generate_wallet() -> dict:
    """Generate a pseudo‑random wallet with an address and private key."""
    return {
        "address": "0x" + secrets.token_hex(20),
        "private_key": secrets.token_hex(32),
    }


def save_wallet(wallet: dict, filename: str = "wallet_ledger.json") -> None:
    """Persist a wallet into a JSON ledger.

    Parameters
    ----------
    wallet:
        The wallet dictionary to append to the ledger.
    filename:
        Path to the JSON file relative to the backend root.  Defaults
        to ``wallet_ledger.json``.
    """
    # Determine absolute path for the ledger file relative to this
    # package.  This ensures we write into the genesis_deploy
    # directory rather than the current working directory.
    ledger_path = Path(__file__).resolve().parent.parent / filename
    if ledger_path.exists():
        with ledger_path.open("r") as f:
            try:
                ledger = json.load(f)
            except Exception:
                ledger = []
    else:
        ledger = []
    ledger.append(wallet)
    with ledger_path.open("w") as f:
        json.dump(ledger, f, indent=2)