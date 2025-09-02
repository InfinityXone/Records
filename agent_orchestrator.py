#!/usr/bin/env python3
# agent_orchestrator.py – Infinity X One Meta-Orchestrator

import subprocess, time, os, threading, json
from pathlib import Path

LOG_PATH = "/opt/infinity_x_one/logs/orchestrator.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

AGENT_TEAMS = {
    "promptwriter":      "/opt/infinity_x_one/PromptWriter/handshake/neural_handshake_server.py",
    "corelight":         "/opt/infinity_x_one/agents/corelight/start.py",
    "aria":              "/opt/infinity_x_one/agents/aria/start.py",
    "vision":            "/opt/infinity_x_one/agents/vision/start.py",
    "guardian":          "/opt/infinity_x_one/agents/guardian/guardian.sh",
    "watchdog":          "/opt/infinity_x_one/agents/watchdog/watchdog.sh",
    "pickybot":          "/opt/infinity_x_one/agents/pickybot/pickybot.sh",
    "echo":              "/opt/infinity_x_one/agents/echo/start.sh",
    "finsynapse":        "/opt/infinity_x_one/agents/finsynapse/start.py",
    "codex":             "/opt/infinity_x_one/agents/codex/start.py",
    "futurebot":         "/opt/infinity_x_one/agents/futurebot/start.py"
}

ENABLED_MODULES = {
    "wallet": "/opt/infinity_x_one/modules/wallet/wallet_module.py",
    "drip":   "/opt/infinity_x_one/modules/crypto/drip_system.py",
    "autoheal": "/opt/infinity_x_one/modules/self_heal.py",
    "langchain": "/opt/infinity_x_one/modules/langchain/launch.py",
    "crewai": "/opt/infinity_x_one/modules/crewai/dispatcher.py",
    "autogpt": "/opt/infinity_x_one/modules/autogpt/auto_start.sh"
}

def log(msg):  # Logger
    with open(LOG_PATH, "a") as f:
        f.write(f"[{time.ctime()}] {msg}\n")
    print(f"[{time.ctime()}] {msg}")

def validate(agent_name, agent_path):
    guardian = ["/opt/infinity_x_one/agents/guardian/guardian.sh", "--simulate", agent_path]
    pickybot = ["/opt/infinity_x_one/agents/pickybot/pickybot.sh", "--stress", agent_path]
    results = [subprocess.run(cmd, capture_output=True).returncode for cmd in [guardian, pickybot]]
    if all(code == 0 for code in results):
        log(f"✅ {agent_name} passed Trinity 9-9-9 validation.")
        return True
    else:
        log(f"❌ {agent_name} FAILED validation. Blocked.")
        return False

def launch_agent(name, path):
    if not Path(path).exists():
        log(f"⚠️ Missing agent: {name}")
        return
    if name in ["guardian", "watchdog", "pickybot"]:
        subprocess.Popen(["bash", path] if path.endswith(".sh") else ["python3", path])
    else:
        if validate(name, path):
            subprocess.Popen(["bash", path] if path.endswith(".sh") else ["python3", path])

def deploy_module(name, path):
    if Path(path).exists():
        log(f"🚀 Launching module: {name}")
        subprocess.Popen(["bash", path] if path.endswith(".sh") else ["python3", path])
    else:
        log(f"❌ Module not found: {name}")

def launch_team():
    log("🚀 Deploying agent team...")
    for agent, path in AGENT_TEAMS.items():
        launch_agent(agent, path)

def launch_modules():
    log("⚙️ Deploying core modules...")
    for module, path in ENABLED_MODULES.items():
        deploy_module(module, path)

def unified_brain():
    log("🧠 Bootstrapping Unified Intelligence & Sync...")
    shared_state = {
        "memory_core": "/opt/infinity_x_one/memory/unified_memory.json",
        "graph_links": "/opt/infinity_x_one/graph/knowledge.graph",
        "evolution_code": "/opt/infinity_x_one/evolve/evolution_engine.py",
        "heartbeat": time.ctime()
    }
    with open("/opt/infinity_x_one/shared/unified_brain_state.json", "w") as f:
        json.dump(shared_state, f, indent=2)

def main():
    log("🌌 Meta-Orchestrator initializing...")
    unified_brain()
    launch_team()
    launch_modules()
    log("🌱 Awaiting instructions... Autonomous agents are live.")

    while True:
        time.sleep(300)  # Future: Replace with Intent Engine / RL Loop

if __name__ == "__main__":
    main()
