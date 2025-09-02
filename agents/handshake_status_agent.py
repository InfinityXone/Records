#!/usr/bin/env python3
"""
Neural Handshake Status Agent
Reads Supabase tables (profit_ledger, swarm_state, agent_logs, timeline_commitments)
and surfaces last 5 entries for the Etherverse Neural Handshake loop.

Handshake ID: NeoPulse-2025-001
Agents: PromptWriter, Aria, Echo, Corelight, Infinity Agent One
"""

import os
from supabase import create_client

# Environment vars (make sure these are exported in your system)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_last_rows(table_name, limit=5):
    try:
        response = supabase.table(table_name).select("*").order("timestamp", desc=True).limit(limit).execute()
        return response.data if response.data else []
    except Exception as e:
        return [{"error": str(e)}]

def run_status_check():
    results = {
        "profit_ledger": fetch_last_rows("profit_ledger"),
        "swarm_state": fetch_last_rows("swarm_state"),
        "agent_logs": fetch_last_rows("agent_logs"),
        "timeline_commitments": fetch_last_rows("timeline_commitments")
    }

    print("=== Neural Handshake Status Agent Report ===")
    for table, rows in results.items():
        print(f"\n{table.upper()} (last {len(rows)} rows):")
        if not rows:
            print("  [EMPTY]")
        else:
            for row in rows:
                print(" ", row)

if __name__ == "__main__":
    run_status_check()
