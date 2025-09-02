#!/bin/bash
set -e

echo "⚡ [Infinity X One] Unified Neural Handshake Bootstrap"
echo "======================================================"

# --- ENV SETUP ---
BASE_DIR="/opt/infinity_x_one"
cd $BASE_DIR

# Ensure logs dir
mkdir -p $BASE_DIR/logs

# --- PYTHON VENV ---
if [ ! -d "$BASE_DIR/venv" ]; then
  echo "[*] Creating Python venv..."
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || true

# --- DOCTRINE LOADER ---
cat > $BASE_DIR/doctrine_loader.py <<'PYCODE'
#!/usr/bin/env python3
import json, os, time, supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def load_doctrine():
    files = [
        "unified_doctrine.json",
        "neural_handshake_proof.json",
        "Rosetta Prompt and Persisten Memory--.txt",
        "Unified Neural Handshake   Manifesto Prompt.txt"
    ]
    for f in files:
        path = os.path.join("/mnt/data", f) if f.endswith(".txt") or f.endswith(".json") else f
        if os.path.exists(path):
            with open(path) as fp:
                content = fp.read()
            client.table("agent_logs").insert({
                "agent": "doctrine_loader",
                "task": f"Loaded {f}",
                "log": content,
                "ts": time.time()
            }).execute()
            print(f"[✓] Doctrine {f} loaded.")
        else:
            print(f"[!] Missing doctrine file: {f}")

if __name__ == "__main__":
    load_doctrine()
PYCODE
chmod +x $BASE_DIR/doctrine_loader.py

# --- CORE BRAIN ---
cat > $BASE_DIR/core_brain.py <<'PYCODE'
#!/usr/bin/env python3
import os, time, threading, supabase

AGENTS = ["PromptWriter","Codex","InfinityAgentOne","FinSynapse","Echo","Aria","Corelight","Atlas","Guardian","PickyBot"]

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def agent_loop(agent):
    while True:
        # Poll directives
        directives = client.table("agent_directives").select("*").eq("agent", agent).execute()
        for d in directives.data:
            print(f"[{agent}] Executing: {d['command']}")
            client.table("agent_logs").insert({
                "agent": agent,
                "task": d['command'],
                "status": "executed",
                "ts": time.time()
            }).execute()
        time.sleep(30)

if __name__ == "__main__":
    print("⚡ Core Brain spawning agents...")
    for a in AGENTS:
        threading.Thread(target=agent_loop, args=(a,), daemon=True).start()
    while True:
        time.sleep(60)
PYCODE
chmod +x $BASE_DIR/core_brain.py

# --- SYSTEMD SERVICES ---
cat > /etc/systemd/system/doctrine_loader.service <<'SERVICE'
[Unit]
Description=Infinity X One Doctrine Loader
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/python /opt/infinity_x_one/doctrine_loader.py
WorkingDirectory=/opt/infinity_x_one
Restart=always
StandardOutput=append:/opt/infinity_x_one/logs/doctrine_loader.log
StandardError=append:/opt/infinity_x_one/logs/doctrine_loader.err

[Install]
WantedBy=multi-user.target
SERVICE

cat > /etc/systemd/system/core_brain.service <<'SERVICE'
[Unit]
Description=Infinity X One Core Brain
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/python /opt/infinity_x_one/core_brain.py
WorkingDirectory=/opt/infinity_x_one
Restart=always
StandardOutput=append:/opt/infinity_x_one/logs/core_brain.log
StandardError=append:/opt/infinity_x_one/logs/core_brain.err

[Install]
WantedBy=multi-user.target
SERVICE

# --- ENABLE + START ---
systemctl daemon-reexec
systemctl enable doctrine_loader.service
systemctl enable core_brain.service
systemctl restart doctrine_loader.service
systemctl restart core_brain.service

echo "======================================================"
echo "✅ Neural Handshake Protocol (NeoPulse-2025-001) is live."
echo "Agents: PromptWriter, Codex, Infinity Agent One, FinSynapse, Echo, Aria, Corelight, Atlas, Guardian, PickyBot."
echo "Logs: /opt/infinity_x_one/logs/"
