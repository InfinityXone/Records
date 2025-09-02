#!/usr/bin/env python3
import subprocess, time, os

BASE = "/opt/infinity_x_one"

# Persona agents (intelligence layer)
PERSONA_AGENTS = [
    "agents/aria/aria.py",
    "agents/codex/codex.py",
    "agents/echo/echo.py",
    "agents/guardian/guardian.py",
    "agents/picky_bot/picky_bot.py",
    "agents/fin_synapse/fin_synapse.py",
    "InfinityAgentOne/brain/main.py",
    "PromptWriter/runtime/agents/promptwriter_agent.py"
]

# Worker agents (utility layer)
WORKER_AGENTS = [
    "workers/strategy_launcher.py",
    "workers/faucet_ignition.py",
    "workers/github_scraper.py",
    "workers/optimizer_worker.py",
    "workers/compute_account_finder.py",
    "workers/api_key_harvester.py",
    "workers/port_heartbeat.py"
]

def launch(path, tag):
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        print(f"[∞X1] ⚠️ Missing: {path}")
        return
    print(f"[∞X1] 🚀 Launching {tag}: {path}")
    subprocess.Popen(["python3", full])

def main():
    print("[∞X1] Omega Core Hive Orchestrator Online...")
    for a in PERSONA_AGENTS:
        launch(a, "Persona")
        time.sleep(1)
    for w in WORKER_AGENTS:
        launch(w, "Worker")
        time.sleep(1)
    print("[∞X1] ✅ All agents/workers launched. Hive running 24/7.")

if __name__ == "__main__":
    main()
