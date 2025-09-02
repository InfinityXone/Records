#!/opt/infinity_x_one/venv/bin/python3
from fastapi import FastAPI, Request
import subprocess, json, os
app = FastAPI(title="Infinity X One Handshake")

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
  "faucet":"backend/workers/faucet_worker.py",
  "keyharvester":"backend/workers/key_harvester.py",
  "atlas":"backend/workers/atlas_bot.py"
}

@app.post("/invoke/{agent}")
async def invoke(agent: str, request: Request):
    payload = await request.json()
    if agent not in WORKERS:
        return {"error": f"unknown agent: {agent}"}
    subprocess.Popen(["/opt/infinity_x_one/venv/bin/python3", WORKERS[agent], json.dumps(payload)])
    return {"status":"queued","agent":agent}

@app.get("/status")
def status():
    return {"status":"ok","agents":list(WORKERS.keys())}
