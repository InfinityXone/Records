#!/usr/bin/env python3
import json, datetime
from web3 import Web3
from supabase import create_client, Client

CFG = json.load(open("/opt/infinity_x_one/03_Systems/FaucetSwarm/faucet_config.json"))

w3 = Web3(Web3.HTTPProvider(CFG["rpc_url"]))

SUPABASE_URL = "https://xzxkyrdelmbqlcucmzpx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6eGt5cmRlbG1icWxjdWNtenB4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTE0MTE0NSwiZXhwIjoyMDcwNzE3MTQ1fQ.WwE58HIpKZ8O9a244yt79jNuSyThkYODGCPL7a7u2_w"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_balance(wallet, balance):
    supabase.table("agent_logs").insert({
        "ts": datetime.datetime.utcnow().isoformat(),
        "agent_id": wallet,
        "action": "wallet_balance",
        "details": {"balance": str(balance)}
    }).execute()

def track_wallets():
    for w in CFG["wallets"]:
        addr = w["address"]
        bal = w3.eth.get_balance(addr)
        eth = w3.from_wei(bal, 'ether')
        print(f"💰 Wallet {addr} balance: {eth} ETH")
        log_balance(addr, eth)

if __name__ == "__main__":
    track_wallets()

# To save in nano: CTRL+O then Enter, then CTRL+X to exit
