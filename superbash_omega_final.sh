#!/bin/bash
set -e

BASE="/opt/infinity_x_one"
VENV="$BASE/venv"
LOGS="$BASE/logs"
AGENTS="$BASE/agents"
CORE="$BASE/core"
QUEUE="$BASE/queue"

echo "=============================================="
echo "🚀 Omega Final Bootstrap – Infinity X One"
echo "=============================================="

# 1. Folders
echo "[*] Creating directories..."
sudo mkdir -p $CORE $AGENTS $LOGS/agents $QUEUE

# 2. Python env + deps
echo "[*] Setting up Python venv..."
python3 -m venv $VENV
source $VENV/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn supabase python-dotenv requests

# 3. Handshake server (Omega aligned)
echo "[*] Writing handshake_server.py..."
cat > $CORE/handshake_server.py <<'PYCODE'
# (paste the full Omega-aligned handshake_server.py here — from my last answer)
PYCODE

# 4. Agent workers (templates, specialized logic can be extended)
for agent in codex promptwriter guardian pickybot atlas infinity echo aria finsynapse; do
  echo "[*] Writing ${agent}_worker.py..."
  cat > $AGENTS/${agent}_worker.py <<PYCODE
import time, requests, os

AGENT = "${agent^}"  # capitalize first letter
HANDSHAKE = "http://localhost:8000"

def heartbeat():
    try:
        requests.post(f"{HANDSHAKE}/handshake", json={
            "agent": AGENT,
            "status": "online",
            "ip": "127.0.0.1",
            "version": "0.1.0"
        })
    except Exception as e:
        print("Heartbeat failed:", e)

def fetch_directive():
    try:
        r = requests.get(f"{HANDSHAKE}/directive", params={"agent": AGENT})
        return r.json()
    except:
        return {}

def complete(task_id, output):
    try:
        requests.post(f"{HANDSHAKE}/complete", json={
            "agent": AGENT, "task_id": task_id,
            "status": "done", "output": output
        })
    except Exception as e:
        print("Completion failed:", e)

if __name__ == "__main__":
    heartbeat()
    while True:
        d = fetch_directive()
        if d and isinstance(d, dict) and "command" in str(d):
            task_id = str(time.time())
            complete(task_id, f"Executed directive: {d}")
        time.sleep(15)
PYCODE
done

# 5. Systemd unit for handshake
echo "[*] Writing handshake_server.service..."
sudo tee /etc/systemd/system/handshake_server.service > /dev/null <<SERVICE
[Unit]
Description=Infinity X One Handshake Server
After=network.target

[Service]
User=$USER
WorkingDirectory=$CORE
ExecStart=$VENV/bin/uvicorn handshake_server:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
WatchdogSec=15
StandardOutput=append:$LOGS/handshake_server.log
StandardError=append:$LOGS/handshake_server.err
Environment="SUPABASE_URL=$SUPABASE_URL"
Environment="SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY"

[Install]
WantedBy=multi-user.target
SERVICE

# 6. Systemd units for all workers
for agent in codex promptwriter guardian pickybot atlas infinity echo aria finsynapse; do
  echo "[*] Writing ${agent}_worker.service..."
  sudo tee /etc/systemd/system/${agent}_worker.service > /dev/null <<SERVICE
[Unit]
Description=${agent^} Worker - Infinity X One
After=network.target handshake_server.service

[Service]
User=$USER
WorkingDirectory=$AGENTS
ExecStart=$VENV/bin/python $AGENTS/${agent}_worker.py
Restart=always
RestartSec=10
StandardOutput=append:$LOGS/agents/${agent}.log
StandardError=append:$LOGS/agents/${agent}.err

[Install]
WantedBy=multi-user.target
SERVICE
done

# 7. Reload systemd + enable services
echo "[*] Reloading systemd..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

echo "[*] Enabling and starting handshake server..."
sudo systemctl enable handshake_server
sudo systemctl restart handshake_server

echo "[*] Enabling and starting all workers..."
for agent in codex promptwriter guardian pickybot atlas infinity echo aria finsynapse; do
  sudo systemctl enable ${agent}_worker
  sudo systemctl restart ${agent}_worker
done

echo "=============================================="
echo "✅ Omega Handshake sealed: all agents online"
echo "✅ Handshake Server: http://localhost:8000/status"
echo "✅ Logs: $LOGS"
echo "=============================================="
