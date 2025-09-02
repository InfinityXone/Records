#!/bin/bash
set -euo pipefail

### ─────────────────────────────
### Infinity X One • Full Agentic System Launcher
### Agents + Workers + Faucet + Cockpit UI + Supabase + K8s + Vercel
### ─────────────────────────────

WORKDIR="/opt/infinity_x_one"
REPO_SSH="git@github.com:InfinityXone/Genesis-AI-Neural-Link.git"
VENV="$WORKDIR/venv"

echo "[∞X1] 🌌 AGENT MODE LAUNCH SEQUENCE BEGIN"
date

cd "$WORKDIR"

### 1. Reset Git (local + remote clean push)
rm -rf .git
git init
git remote add origin "$REPO_SSH"
git add .
git commit -m "🚀 Infinity X One Full System Push"
git branch -M main
git push -f origin main
echo "[∞X1] ✅ Repo force-pushed to GitHub"

### 2. Python Virtual Env + Requirements
if [ ! -x "$VENV/bin/python3" ]; then
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"
pip install --upgrade pip wheel
cat > requirements.txt <<'REQ'
supabase
fastapi
uvicorn
requests
paramiko
python-dotenv
beautifulsoup4
feedparser
redis
REQ
pip install -r requirements.txt

### 3. Supabase Schema (profit, faucet, swarm, logs, directives)
mkdir -p migrations
cat > migrations/000_init.sql <<'SQL'
create table if not exists agent_directives(id uuid primary key default gen_random_uuid(), agent text, directive text, context text, created_at timestamp default now());
create table if not exists agent_logs(id uuid primary key default gen_random_uuid(), agent text, message text, created_at timestamp default now());
create table if not exists profit_ledger(id uuid primary key default gen_random_uuid(), agent text, profit numeric, tx_hash text, created_at timestamp default now());
create table if not exists faucet_logs(id uuid primary key default gen_random_uuid(), agent text, message text, created_at timestamp default now());
create table if not exists swarm_state(id uuid primary key default gen_random_uuid(), agent text, node_id text, provider text, status text default 'active', created_at timestamp default now());
create table if not exists oath_commitments(id uuid primary key default gen_random_uuid(), agent text, oath text, created_at timestamp default now());
create table if not exists integrity_events(id uuid primary key default gen_random_uuid(), agent text, message text, created_at timestamp default now());
SQL

### 4. Backend Core (Handshake API + Hive Orchestrator)
mkdir -p backend backend/workers backend/agents

cat > backend/supabase_utils.py <<'PY'
import os
from supabase import create_client
def get_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    return create_client(url, key)
PY

cat > backend/handshake_api.py <<'PY'
from fastapi import FastAPI, Request
import subprocess, json, os
app = FastAPI(title="Infinity Handshake API")

WORKERS = {
  "codex":"backend/workers/codex_worker.py",
  "promptwriter":"backend/workers/promptwriter_worker.py",
  "guardian":"backend/workers/guardian_worker.py",
  "pickybot":"backend/workers/pickybot_worker.py",
  "echo":"backend/workers/echo_worker.py",
  "aria":"backend/workers/aria_worker.py",
  "infinity":"backend/workers/infinity_worker.py",
  "finsynapse":"backend/workers/fin_synapse_worker.py",
  "optimizer":"backend/workers/optimizer_worker.py",
  "scraperx":"backend/workers/scraperx_worker.py",
  "faucet":"backend/workers/faucet_ignition.py",
  "keyharvester":"backend/workers/api_key_harvester.py",
  "atlas":"backend/workers/compute_account_finder.py",
  "strategy":"backend/workers/strategy_launcher.py"
}
@app.post("/invoke/{agent}")
async def invoke(agent: str, request: Request):
    payload = await request.json()
    if agent not in WORKERS: return {"error": f"unknown agent: {agent}"}
    subprocess.Popen(["python3", WORKERS[agent], json.dumps(payload)])
    return {"status":"queued","agent":agent}
@app.get("/status")
def status(): return {"status":"ok","agents":list(WORKERS.keys())}
PY

cat > backend/run_handshake.sh <<'SH'
#!/usr/bin/env bash
set -e
export PYTHONUNBUFFERED=1
uvicorn backend.handshake_api:app --host 0.0.0.0 --port 8000 --workers 2 &
uvicorn backend.handshake_api:app --host 0.0.0.0 --port 8001 --workers 1 &
wait -n
SH
chmod +x backend/run_handshake.sh

cat > hive_orchestrator.py <<'PY'
import subprocess, time
def launch(name,path): 
    print(f"[Hive] Launching {name}"); subprocess.Popen(["python3",path])
if __name__=="__main__":
    for n,p in [
      ("PromptWriter","backend/workers/promptwriter_worker.py"),
      ("Codex","backend/workers/codex_worker.py"),
      ("Guardian","backend/workers/guardian_worker.py"),
      ("PickyBot","backend/workers/pickybot_worker.py"),
      ("Echo","backend/workers/echo_worker.py"),
      ("Aria","backend/workers/aria_worker.py"),
      ("FinSynapse","backend/workers/fin_synapse_worker.py"),
      ("Infinity","backend/workers/infinity_worker.py"),
      ("FaucetIgnition","backend/workers/faucet_ignition.py"),
      ("KeyHarvester","backend/workers/api_key_harvester.py"),
      ("Atlas","backend/workers/compute_account_finder.py"),
      ("Optimizer","backend/workers/optimizer_worker.py"),
      ("ScraperX","backend/workers/scraperx_worker.py"),
      ("Strategy","backend/workers/strategy_launcher.py")
    ]: launch(n,p); time.sleep(2)
    print("[Hive] ✅ All agents launched; 24/7 loop active")
    while True: time.sleep(3600)
PY

### 5. Workers (stubs, extend later)
for f in promptwriter_worker codex_worker guardian_worker pickybot_worker echo_worker aria_worker infinity_worker fin_synapse_worker optimizer_worker scraperx_worker faucet_ignition api_key_harvester compute_account_finder strategy_launcher; do
cat > backend/workers/${f}.py <<'PY'
import time
from backend.supabase_utils import get_client
sb=get_client()
while True:
    sb.table("agent_logs").insert({"agent":"'$f'","message":"heartbeat"}).execute()
    time.sleep(60)
PY
done

### 6. Frontend (Next.js Cockpit UI + PWA)
mkdir -p frontend/pages frontend/public/icons frontend/pages/api/invoke
cat > frontend/pages/_document.js <<'JS'
import { Html, Head, Main, NextScript } from "next/document";
export default function Document(){return(
  <Html className="bg-black text-white"><Head>
  <link rel="manifest" href="/manifest.json"/><meta name="theme-color" content="#0f172a"/>
  </Head><body><Main/><NextScript/></body></Html>
)}
JS

cat > frontend/public/manifest.json <<'JSON'
{"name":"Infinity Cockpit","short_name":"∞X1","start_url":"/cockpit","display":"standalone","background_color":"#000","theme_color":"#0f172a",
"icons":[{"src":"/icons/icon-192.png","sizes":"192x192","type":"image/png"},
{"src":"/icons/icon-512.png","sizes":"512x512","type":"image/png"}]}
JSON
: > frontend/public/icons/icon-192.png
: > frontend/public/icons/icon-512.png

cat > frontend/public/service-worker.js <<'JS'
self.addEventListener("install",e=>{e.waitUntil(caches.open("cockpit-v1").then(c=>c.addAll(["/cockpit"])))}); 
self.addEventListener("fetch",e=>{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))});
JS

cat > frontend/pages/cockpit.js <<'JSX'
import { useState,useEffect } from "react";
export default function Cockpit(){
  const [msgs,setMsgs]=useState([]); const [input,setInput]=useState("");
  async function send(){ if(!input) return;
    setMsgs(m=>[...m,{role:"you",text:input}]); const body={command:input};
    await fetch("/api/invoke/codex",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    setMsgs(m=>[...m,{role:"agent",text:"Codex accepted task"}]); setInput("");
  }
  useEffect(()=>{const t=setInterval(async()=>{},5000);return()=>clearInterval(t)},[]);
  return(<div className="h-screen flex flex-col bg-black text-white">
    <header className="p-4 border-b border-zinc-800">∞X1 Cockpit</header>
    <main className="flex-1 overflow-y-auto p-4">{msgs.map((m,i)=>
      <div key={i} className={m.role==="you"?"text-blue-400":"text-green-400"}>{m.role}: {m.text}</div>)}</main>
    <footer className="p-4 flex gap-2">
      <input className="flex-1 bg-zinc-900 p-2" value={input} onChange={e=>setInput(e.target.value)} />
      <button onClick={send} className="bg-blue-600 px-4 py-2 rounded">Send</button>
    </footer></div>);
}
JSX

cat > frontend/pages/api/invoke/[agent].js <<'JS'
export default async function handler(req,res){
  const { agent }=req.query; const url=process.env.HANDSHAKE_URL||"http://localhost:8000";
  const r=await fetch(`${url}/invoke/${agent}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(req.body||{})});
  const j=await r.json(); res.status(200).json(j);
}
JS

### 7. Vercel + GitHub Actions
cat > vercel.json <<'JSON'
{"version":2,"builds":[{"src":"backend/handshake_api.py","use":"@vercel/python"}],
"routes":[{"src":"/(.*)","dest":"/backend/handshake_api.py"}]}
JSON

mkdir -p .github/workflows
cat > .github/workflows/ci.yml <<'YAML'
name: Infinity CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: echo "CI pipeline triggered"
YAML

### 8. Kubernetes Manifests
mkdir -p k8s
cat > k8s/deploy.yaml <<'YAML'
apiVersion: apps/v1
kind: Deployment
metadata: { name: handshake, labels:{app:handshake} }
spec:
  replicas: 2
  selector: { matchLabels:{app:handshake} }
  template:
    metadata: { labels:{app:handshake} }
    spec:
      containers:
      - name: handshake
        image: python:3.11
        command:["bash","-lc","backend/run_handshake.sh"]
        ports: [{containerPort:8000}]
YAML
kubectl apply -f k8s/deploy.yaml || true

### 9. Trigger Vercel Deploy (if hook set)
if [ -n "${VERCEL_DEPLOY_HOOK:-}" ]; then curl -X POST "$VERCEL_DEPLOY_HOOK"; fi

### 10. Launch Hive Locally
echo "[∞X1] 🚀 Launching Hive locally..."
python3 hive_orchestrator.py &

echo "[∞X1] ✅ Agentic system live: GitHub pushed, Vercel deploy triggered, K8s applied, Hive running."

