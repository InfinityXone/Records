"""Wallet management utilities for Infinity X One.

This module provides simple wallet generation and assignment logic for
agents.  Each wallet consists of a pseudo‑random address and private
key.  Generated wallets are persisted to a local JSON ledger file
(`wallet_ledger.json`) so the same keys can be reused on subsequent
runs.  In production you should replace this with a secure key
management service or blockchain wallet provider.
"""

from .generator import generate_wallet, save_wallet  # noqa: F401
from .manager import assign_wallet_to_agent, load_wallets  # noqa: F401