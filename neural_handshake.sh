#!/bin/bash
echo "🧠 [InfinityXone] Initializing Neural Handshake..."

BASE_DIR="/opt/infinity_x_one"
AGENTS_DIR="$BASE_DIR/agents"
SHARED_HEARTBEAT="$BASE_DIR/shared/heartbeat"
SHARED_MEMORY="$BASE_DIR/shared/memory"
SHARED_INTENTS="$BASE_DIR/shared/intents"

mkdir -p "$SHARED_HEARTBEAT" "$SHARED_MEMORY" "$SHARED_INTENTS"

# Define agents involved in the handshake
AGENTS=("aria" "infinity_agent_one" "codex" "anima" "corelight" "fin_synapse" "guardian" "echo" "futurebot")

timestamp=$(date +"%Y-%m-%d %H:%M:%S")

for agent in "${AGENTS[@]}"; do
  echo "🔗 Handshaking with: $agent"

  AGENT_DIR="$AGENTS_DIR/$agent"
  AGENT_LOG="$SHARED_HEARTBEAT/${agent}_handshake.log"
  AGENT_MEM="$SHARED_MEMORY/${agent}_state.json"
  AGENT_INTENT="$SHARED_INTENTS/${agent}_intent.json"

  # Initialize logs and shared files
  echo "{ \"agent\": \"$agent\", \"status\": \"linked\", \"timestamp\": \"$timestamp\" }" > "$AGENT_LOG"
  echo "{ \"memory\": [], \"status\": \"idle\", \"last_updated\": \"$timestamp\" }" > "$AGENT_MEM"
  echo "{ \"next_action\": \"\", \"priority\": 0, \"timestamp\": \"$timestamp\" }" > "$AGENT_INTENT"

done

# Global Heartbeat File
echo "{ \"heartbeat\": \"online\", \"timestamp\": \"$timestamp\" }" > "$SHARED_HEARTBEAT/global_heartbeat.json"

echo "✅ Neural Handshake Completed for All Agents"
