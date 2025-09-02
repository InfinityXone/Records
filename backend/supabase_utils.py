"""Utilities for interacting with Supabase.

This module centralises the creation of a Supabase client and provides a few
convenience functions for inserting logs and fetching directives.  It expects
certain environment variables to be defined at runtime:

* `SUPABASE_URL` – The base URL of your Supabase project
* `SUPABASE_SERVICE_ROLE_KEY` – A service‑role API key with read/write access
* `SUPABASE_ANON_KEY` – Optional anonymous key for client‑side usage
"""

import os
import datetime
from typing import Any, Dict, List, Optional

try:
    from supabase import create_client  # type: ignore
except ImportError:
    # In case supabase library is not installed.  The worker should install it via requirements.
    create_client = None  # type: ignore


def get_client():
    """Create and return a Supabase client.

    Raises:
        RuntimeError: if required environment variables are missing or the library is unavailable.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in the environment")
    if create_client is None:
        raise RuntimeError(
            "supabase library is not installed; add `supabase-py` to your dependencies"
        )
    return create_client(url, key)


def insert_log(table: str, data: Dict[str, Any]) -> None:
    """Insert a row into a Supabase table.

    This helper wraps `supabase.table(...).insert(...).execute()` and adds a timestamp.

    Args:
        table: The name of the Supabase table.
        data: A dictionary of values to insert.  A `ts` field will be added automatically.
    """
    client = get_client()
    payload = data.copy()
    payload.setdefault("ts", datetime.datetime.utcnow().isoformat())
    client.table(table).insert(payload).execute()


def fetch_pending_directives(agent: str) -> List[Dict[str, Any]]:
    """Fetch directives for a specific agent that are marked as pending.

    Args:
        agent: The agent name to filter on.

    Returns:
        A list of directive objects ordered by creation time.
    """
    client = get_client()
    response = (
        client.table("agent_directives")
        .select("id, command, payload")
        .eq("agent", agent)
        .eq("status", "pending")
        .order("timestamp", desc=False)
        .execute()
    )
    return response.data or []


def mark_directive_complete(directive_id: int) -> None:
    """Mark a directive as complete.

    Args:
        directive_id: The primary key of the directive to update.
    """
    client = get_client()
    client.table("agent_directives").update({"status": "complete"}).eq("id", directive_id).execute()
