#!/bin/bash

# ===== Neural Handshake Loader Parser v1.0 =====
# ✅ Safely parse and validate JSON handshake file
# 📁 File: /opt/infinity_x_one/genesis_neural_handshake.json

HANDSHAKE_FILE="/opt/infinity_x_one/genesis_neural_handshake.json"

# Ensure jq is available
if ! command -v jq &> /dev/null; then
  echo "❌ ERROR: jq is not installed. Please run: sudo apt install jq"
  exit 1
fi

# Validate file existence
if [[ ! -f "$HANDSHAKE_FILE" ]]; then
  echo "❌ ERROR: Handshake file not found: $HANDSHAKE_FILE"
  exit 1
fi

echo "🧠 Parsing: $HANDSHAKE_FILE"
echo "--------------------------------------"

# Output full parsed structure for GPT analysis
jq . "$HANDSHAKE_FILE"

echo "--------------------------------------"
echo "🔎 Extracting critical parameters..."

echo "📌 Traits:"
jq -r '.agent_replication.traits[]' "$HANDSHAKE_FILE"

echo "📌 Template:"
jq -r '.agent_replication.template' "$HANDSHAKE_FILE"

echo "📌 Agent Count:"
jq -r '.agent_replication.initialAgentsToSpawn' "$HANDSHAKE_FILE"

echo "📌 Deployment Phases:"
jq -r '.emergency_protocol.deployment_phases[]' "$HANDSHAKE_FILE"

echo "✅ Handshake parsed successfully. Ready for orchestration."
