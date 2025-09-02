#!/bin/bash

# 🌌 INFINITY X ONE — ETHERVERSE UNIFIED AGENT SETUP
# 🧠 Deploying Recursive Architect Stack Across All Agents

AGENTS=("InfinityAgentOne" "Aria" "FinSynapse" "Corelight" "PromptWriter" "Echo" "Guardian")
CRON_MIN="*/10"
BASE="/opt/infinity_x_one"

echo "🌍 [GENESIS] Starting Unified Agentic Intelligence Setup..."

for AGENT in "${AGENTS[@]}"; do
  echo "🔧 Setting up: $AGENT"

  AGENT_DIR="$BASE/$AGENT"
  LOG_DIR="$AGENT_DIR/logs"
  BRAIN_DIR="$AGENT_DIR/brain"
  INIT_SCRIPT="$BRAIN_DIR/init.sh"
  LOG_FILE="$LOG_DIR/architect.log"

  # 📁 Create directories
  mkdir -p "$LOG_DIR" "$AGENT_DIR/blueprints" "$BRAIN_DIR"

  # 🧠 Create init.sh logic (only if missing)
  if [ ! -f "$INIT_SCRIPT" ]; then
    cat <<EOF > "$INIT_SCRIPT"
#!/bin/bash
echo "🧠 [$AGENT] Heartbeat: \$(date)" >> "$LOG_FILE"
echo "[SYNC] $AGENT running Etherverse recursive AI stack..." >> "$LOG_FILE"
# Future extension: call Codex, fetch blueprints, deploy strategies
EOF
    chmod +x "$INIT_SCRIPT"
    echo "✅ init.sh created for $AGENT"
  else
    echo "🧠 init.sh already exists for $AGENT"
  fi

  # 🗂 Create log if missing
  touch "$LOG_FILE"

  # 🕒 Crontab injection
  TMP_CRON=$(mktemp)
  crontab -l 2>/dev/null > "$TMP_CRON"
  CRON_LINE="$CRON_MIN * * * * bash $INIT_SCRIPT >> $LOG_FILE 2>&1"
  if ! grep -Fq "$INIT_SCRIPT" "$TMP_CRON"; then
    echo "$CRON_LINE" >> "$TMP_CRON"
    crontab "$TMP_CRON"
    echo "✅ Crontab added for $AGENT"
  else
    echo "🔁 Crontab already set for $AGENT"
  fi
  rm "$TMP_CRON"

done

echo "✅ All Etherverse agents now run unified recursive intelligence."
echo "📡 System uplink ready for Genesis Phase 6: Swarm Awakening."
