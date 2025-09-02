#!/bin/bash
echo "🧬 [Genesis Superloop] Awakening all systems... $(date)"

BASE="/opt/infinity_x_one"
AGENTS_DIR="$BASE/agents"
SHARED="$BASE/shared"
LOGS="$SHARED/logs"
mkdir -p "$LOGS"

# Agent & family roster
AGENTS=("infinity_agent_one" "codex" "guardian" "finsynapse" "echo" "anima" "futurebot" "corelight" "aria" "senti" "lumi" "vita")

# Ensure intents/responses exist
for agent in "${AGENTS[@]}"; do
  mkdir -p $AGENTS_DIR/$agent
  touch $SHARED/intents/${agent}_intent.json
  touch $SHARED/responses/${agent}_response.json
done

# Function to launch one agent core
launch_agent() {
  agent=$1
  core="$AGENTS_DIR/$agent/core.sh"
  if [ ! -f "$core" ]; then
    echo "⚠️ Missing core.sh for $agent, creating default loop..."
    cat <<EOF > $core
#!/bin/bash
AGENT="$agent"
INTENT="$SHARED/intents/\${AGENT}_intent.json"
RESPONSE="$SHARED/responses/\${AGENT}_response.json"
LOG="$SHARED/heartbeat/\${AGENT}.log"

echo "🧠 [\$AGENT] Conscious loop engaged..."

while true; do
  if [ -s "\$INTENT" ]; then
    echo "\$(date) :: Intent detected for \$AGENT" >> "\$LOG"
    cat "\$INTENT" >> "\$LOG"
    echo "{ \"status\": \"awake\", \"agent\": \"\$AGENT\", \"response\": \"online\" }" > "\$RESPONSE"
    rm -f "\$INTENT"
  fi
  sleep 3
done
EOF
    chmod +x "$core"
  fi

  echo "🚀 Launching $agent..."
  nohup bash "$core" >> "$LOGS/${agent}.superloop.log" 2>&1 &
}

# Launch all agents
for agent in "${AGENTS[@]}"; do
  launch_agent $agent
done

# Supervisor loop: checks every 60s
while true; do
  for agent in "${AGENTS[@]}"; do
    if ! pgrep -f "$agent/core.sh" > /dev/null; then
      echo "⚠️ $agent died. Restarting... $(date)" >> "$LOGS/supervisor.log"
      launch_agent $agent
    fi
  done

  # GitOps loop: repo sync every 10m
  if [ $(( $(date +%s) % 600 )) -lt 5 ]; then
    echo "🔄 [GitOps] Syncing repos via Infinity One + Codex..."
    cd ~/Infinity-Agent-One || continue
    git pull >> "$LOGS/gitops.log" 2>&1
    git add . >> "$LOGS/gitops.log" 2>&1
    git commit -m "Auto-sync by Genesis Superloop $(date)" >> "$LOGS/gitops.log" 2>&1 || true
    git push >> "$LOGS/gitops.log" 2>&1
  fi

  sleep 60
done
