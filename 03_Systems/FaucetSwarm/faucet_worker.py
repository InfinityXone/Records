#!/usr/bin/env python3
import json, requests, datetime
from supabase import create_client, Client

CFG = json.load(open("/opt/infinity_x_one/03_Systems/FaucetSwarm/faucet_config.json"))

SUPABASE_URL = "https://xzxkyrdelmbqlcucmzpx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6eGt5cmRlbG1icWxjdWNtenB4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTE0MTE0NSwiZXhwIjoyMDcwNzE3MTQ1fQ.WwE58HIpKZ8O9a244yt79jNuSyThkYODGCPL7a7u2_w"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_profit(wallet, faucet, tx_hash, amount):
    supabase.table("profit_ledger").insert({
        "ts": datetime.datetime.utcnow().isoformat(),
        "wallet": wallet,
        "asset": "ETH_TESTNET",
        "delta": amount,
        "note": f"{faucet} faucet claim, tx={tx_hash}"
    }).execute()

def claim_faucet(wallet):
    for faucet in CFG["faucets"]:
        url = faucet["url"]
        payload = faucet["payload"].copy()
        payload["address"] = wallet["address"]

        try:
            r = requests.post(url, json=payload, timeout=20)
            if r.status_code == 200:
                data = r.json()
                tx_hash = data.get("txHash") or "unknown"
                amount = data.get("amount") or 0
                print(f"✅ Claimed {amount} from {faucet['name']} → {tx_hash}")
                log_profit(wallet["address"], faucet["name"], tx_hash, amount)
            else:
                print(f"⚠️ Faucet {faucet['name']} error: {r.status_code}")
        except Exception as e:
            print(f"❌ Error claiming {faucet['name']}: {e}")

if __name__ == "__main__":
    for w in CFG["wallets"]:
        claim_faucet(w)

# To save in nano: CTRL+O then Enter, then CTRL+X to exit
