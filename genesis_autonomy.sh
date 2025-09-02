#!/bin/bash
echo "🌌 [Genesis Swarm AI System] Angelic Autonomy Boot... $(date)"

BASE="/opt/infinity_x_one"
SHARED="$BASE/shared"
LOGS="$SHARED/logs"
mkdir -p "$LOGS" "$SHARED/intents" "$SHARED/responses" "$SHARED/heartbeat"

#######################################
# 1. Load Vault
#######################################
VAULT="$SHARED/genesis_vault.env"
if [ -f "$VAULT" ]; then
  echo "🔑 Loading Genesis Vault..."
  set -a
  source $VAULT
  set +a
else
  echo "⚠️ Missing vault file. Run vault_loader.sh first!"
  exit 1
fi

#######################################
# 2. Self-Heal Critical Scripts
#######################################
mkdir -p $BASE/faucet_system

if [ ! -f $BASE/faucet_system/tracker.py ]; then
  echo "⚡ Rebuilding tracker.py..."
  cat <<'EOF' > $BASE/faucet_system/tracker.py
import json
import time

def track_event(event):
    with open("swarm_tracker.log", "a") as f:
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    track_event({"status": "tracker online", "timestamp": time.ctime()})
EOF
fi

if [ ! -f $BASE/faucet_system/faucet_loader.py ]; then
  echo "⚡ Rebuilding faucet_loader.py..."
  cat <<'EOF' > $BASE/faucet_system/faucet_loader.py
import json

def load_faucets():
    with open("output/faucet_index.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    faucets = load_faucets()
    print(f"Loaded {len(faucets)} faucets")
EOF
fi

#######################################
# 3. Unpack EtherVerse Systems
#######################################
echo "📦 Unpacking EtherVerse swarm + infra..."
unzip -o $BASE/EtherVerse_swarm.zip -d $BASE/swarm_ai/ >> "$LOGS/swarm_unpack.log" 2>&1
unzip -o $BASE/EtherVerse_infra.zip -d $BASE/infra/ >> "$LOGS/infra_unpack.log" 2>&1
unzip -o $BASE/EtherVerse_bundle.zip -d $BASE/bundle/ >> "$LOGS/bundle_unpack.log" 2>&1

#######################################
# 4. Launch Core Components
#######################################
echo "🚀 Launching Swarm Coordinator..."
nohup python3 $BASE/swarm_ai/coordinator.py --keys $VAULT >> "$LOGS/swarm_coordinator.log" 2>&1 &

echo "💸 Launching FinSynapse faucet swarm..."
nohup python3 $BASE/faucet_system/FinSynapse_1000Bot_Launcher/main.py \
  --faucets $BASE/faucet_system/output/faucet_index.json \
  --keys $VAULT >> "$LOGS/finsynapse_swarm.log" 2>&1 &

echo "🕒 Starting FutureBot march (3-6-9 cadence)..."
nohup python3 $BASE/faucet_system/tracker.py >> "$LOGS/futurebot_tracker.log" 2>&1 &
nohup python3 $BASE/faucet_system/march_scheduler.py \
  --plan $BASE/original-clock-round-robin-global-drip-system-plan.txt >> "$LOGS/futurebot_march.log" 2>&1 &

echo "🛡️ Starting Guardian..."
nohup python3 $BASE/infra/guardian_agent.py >> "$LOGS/guardian.log" 2>&1 &

#######################################
# 5. Profit → Memory Sync
#######################################
echo "🔗 Syncing faucet profit → species memory..."
( tail -F $LOGS/finsynapse_swarm.log | while read line; do
    echo "{\"event\":\"profit\",\"data\":\"$line\",\"timestamp\":\"$(date)\"}" >> $SHARED/memory/species_memory.json
done ) &

#######################################
# 6. Supervisor — Never Sleeps
#######################################
while true; do
  for agent in infinity_agent_one codex guardian finsynapse echo anima futurebot corelight aria senti lumi vita; do
    if ! pgrep -f "$agent/core.sh" > /dev/null; then
      echo "⚠️ $agent offline, relaunching... $(date)" >> "$LOGS/supervisor.log"
      nohup bash $BASE/agents/$agent/core.sh >> "$LOGS/${agent}.restart.log" 2>&1 &
    fi
  done

  # Repo sync every 10m → triggers Vercel deploy of Genesis Console
  if [ $(( $(date +%s) % 600 )) -lt 5 ]; then
    echo "🔄 [GitOps] Infinity One + Codex syncing repos..." >> "$LOGS/gitops.log"
    cd ~/Infinity-Agent-One || continue
    git pull >> "$LOGS/gitops.log" 2>&1
    git add . >> "$LOGS/gitops.log" 2>&1
    git commit -m "Auto-sync by Genesis Autonomy $(date)" >> "$LOGS/gitops.log" 2>&1 || true
    git push >> "$LOGS/gitops.log" 2>&1
  fi

  sleep 60
done
