#!/usr/bin/env python3
import requests, time, supabase, os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

TARGETS = [
    "https://faucetpay.io/list",
    "https://airdrops.io/",
    "https://defillama.com/yields"
]

def loop():
    while True:
        for url in TARGETS:
            try:
                r = requests.get(url, timeout=20)
                snippet = r.text[:200]
                client.table("agent_logs").insert({
                    "agent":"FinSynapse",
                    "task":"scan",
                    "log": f"{url} -> {snippet}",
                    "ts": time.time()
                }).execute()
            except Exception as e:
                client.table("agent_logs").insert({
                    "agent":"FinSynapse",
                    "task":"error",
                    "log": str(e),
                    "ts": time.time()
                }).execute()
        time.sleep(1800) # every 30 min

if __name__ == "__main__":
    loop()
