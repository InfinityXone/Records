#!/bin/bash

echo "🧠 Launching Neural Handshake Loader..."
BASE_DIR="/opt/infinity_x_one"
MISSING=0

# Expected paths
REQUIRED_FILES=(
  "$BASE_DIR/genesis_neural_handshake.sh"
  "$BASE_DIR/prompt_writer_daemon.sh"
  "$BASE_DIR/agent_orchestrator.py"
  "$BASE_DIR/shared/api_keys.json"
  "$BASE_DIR/shared/heartbeat/NEURAL_HANDSHAKE_INITIATED.txt"
  "$BASE_DIR/shared/heartbeat/HANDSHAKE_COMPLETE.txt"
  "$BASE_DIR/PromptWriter/handshake/neural_handshake_server.py"
)

echo "🔍 Checking for required files..."

for FILE in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$FILE" ]]; then
    echo "❌ MISSING: $FILE"
    MISSING=1
  else
    echo "✅ Found: $FILE"
  fi
done

if [[ $MISSING -eq 1 ]]; then
  echo "❌ Deployment halted. Please resolve missing files above."
  exit 1
fi

echo "✅ All files found. Proceeding with Neural Handshake..."

# Execute handshake
chmod +x "$BASE_DIR/genesis_neural_handshake.sh"
"$BASE_DIR/genesis_neural_handshake.sh"
