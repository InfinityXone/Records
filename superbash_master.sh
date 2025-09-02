#!/bin/bash
set -e

echo "🌌 [Infinity X One] Omega Autonomy Bootstrap"
BASE_DIR="/opt/infinity_x_one"
cd $BASE_DIR
mkdir -p logs

# --- Python venv ---
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Requirements
cat > requirements.txt <<'REQ'
supabase
fastapi
uvicorn
requests
paramiko
python-dotenv
REQ
pip install -r requirements.txt

# --- Handshake Server (port 8000) ---
cat > handshake_server.py <<'PY'
from fastapi import FastAPI, Request
import os, time, supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.post("/directive")
async def directive(req: Request):
    data = await req.json()
    client.table("agent_directives").insert({
        "agent": data.get("agent","all"),
        "command": data.get("command"),
        "ts": time.time()
    }).execute()
    return {"status":"ok","echo":data}

@app.get("/status")
async def status():
    return {"handshake":"NeoPulse-2025-001","ts":time.time()}
PY

# --- Deploy Manager ---
cat > deploy_manager.py <<'PY'
import os, time, supabase, subprocess

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def loop():
    while True:
        res = client.table("agent_directives").select("*").eq("agent","deploy_manager").execute()
        for d in res.data:
            cmd = d['command']
            if "deploy" in cmd:
                subprocess.run(["git","add","-A"])
                subprocess.run(["git","commit","-m","auto"])
                subprocess.run(["git","push"])
                subprocess.run(["vercel","--prod"])
                client.table("agent_logs").insert({
                    "agent":"deploy_manager","task":cmd,"status":"executed","ts":time.time()
                }).execute()
        time.sleep(60)

if __name__=="__main__":
    loop()
PY

# --- systemd services ---
cat > /etc/systemd/system/handshake_server.service <<'SERVICE'
[Unit]
Description=Infinity X One Handshake Server
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/uvicorn handshake_server:app --host 0.0.0.0 --port 8000
WorkingDirectory=/opt/infinity_x_one
Restart=always
StandardOutput=append:/opt/infinity_x_one/logs/handshake_server.log
StandardError=append:/opt/infinity_x_one/logs/handshake_server.err

[Install]
WantedBy=multi-user.target
SERVICE

cat > /etc/systemd/system/deploy_manager.service <<'SERVICE'
[Unit]
Description=Infinity X One Deploy Manager
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/python /opt/infinity_x_one/deploy_manager.py
WorkingDirectory=/opt/infinity_x_one
Restart=always
StandardOutput=append:/opt/infinity_x_one/logs/deploy_manager.log
StandardError=append:/opt/infinity_x_one/logs/deploy_manager.err

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reexec
systemctl enable handshake_server deploy_manager
systemctl restart handshake_server deploy_manager

echo "===================================================="
echo "✅ Omega Protocol live. Handshake on :8000"
echo "✅ Deploy Manager active. Autonomy locked."
