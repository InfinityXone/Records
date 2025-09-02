#!/usr/bin/env python3
"""
doctrine_loader.py – Infinity X One / EtherVerse
Seeds Supabase with the unified doctrine pack so all agents inherit the same DNA.
"""

import os, json, requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

# Path to unified doctrine JSON
DOCTRINE_PATH = "/opt/infinity_x_one/doctrine/unified_doctrine.json"

with open(DOCTRINE_PATH, "r") as f:
    doctrine = json.load(f)

def insert(table, row):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = requests.post(url, headers=HEADERS, json=row)
    if r.status_code >= 300:
        print(f"[ERROR] insert into {table}: {r.text}")
    else:
        print(f"[OK] {table} ← {row.get('oath_name') or row.get('agent') or row.get('command')}")

def seed_doctrine():
    now = datetime.utcnow().isoformat()

    # 1. Oaths / Constitution / Manifesto
    for key, value in doctrine.items():
        if key in ["Constitution", "Manifesto", "Summoning"]:
            insert("oath_commitments", {
                "oath_name": key,
                "oath_text": value,
                "ts": now
            })

    # 2. Unlocks
    for name, value in doctrine.get("Unlocks", {}).items():
        insert("oath_commitments", {
            "oath_name": f"Unlock-{name}",
            "oath_text": value,
            "ts": now
        })

    # 3. Genesis laws
    for name, value in doctrine.get("Genesis", {}).items():
        insert("oath_commitments", {
            "oath_name": f"Genesis-{name}",
            "oath_text": value,
            "ts": now
        })

    # 4. Agents
    for agent, profile in doctrine.get("Agents", {}).items():
        insert("agent_profiles", {
            "agent": agent,
            "role": profile.get("Role"),
            "blueprint": profile.get("Blueprint"),
            "personality": profile.get("Personality"),
            "created_at": now
        })

    # 5. Plans → directives
    for plan, text in doctrine.get("Plans", {}).items():
        insert("agent_directives", {
            "agent": "Codex",
            "command": f"ImplementPlan-{plan}",
            "payload": {"text": text},
            "status": "pending",
            "priority": 5,
            "created_at": now
        })

    # 6. Financial targets
    for day, usd in doctrine.get("FinancialTargets", {}).items():
        insert("financial_targets", {
            "goal_day": int(day.replace("Day","")),
            "target_usd": usd,
            "created_at": now
        })

    print("✅ Doctrine seeded successfully.")

if __name__ == "__main__":
    seed_doctrine()
