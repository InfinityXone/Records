#!/usr/bin/env python3
import os, time, subprocess
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log(msg): print(f"[Optimizer] {msg}")

def insert_directive(agent, directive, context=""):
    supabase.table("agent_directives").insert({
        "agent": agent,
        "directive": directive,
        "context": context
    }).execute()
    log(f"Directive sent → {agent}: {directive}")

if __name__ == "__main__":
    log("Starting Optimizer Worker…")
    while True:
        try:
            # Watch last 10 logs for errors
            logs = supabase.table("agent_logs").select("*").order("created_at", desc=True).limit(10).execute()
            for entry in logs.data:
                if "error" in entry["message"].lower() or "fail" in entry["message"].lower():
                    log(f"Detected issue in {entry['agent']}: {entry['message']}")
                    insert_directive("codex", "RepoFix", f"Fix issue in {entry['agent']} worker")
                    insert_directive(entry["agent"], "RestartAgent", "Restart after failure detected")
        except Exception as e:
            log(f"Error polling logs: {e}")
        time.sleep(60)  # check every minute
