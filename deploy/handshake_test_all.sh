#!/bin/bash
# handshake_test_all.sh

BASE="/opt/infinity_x_one"
INTENT_DIR="$BASE/shared/intents"
RESPONSE_DIR="$BASE/shared/responses"
LOG="$BASE/shared/handshake_status.log"
AGENTS=$(ls -1 "$BASE/agents")

echo "🌐 Initiating handshake with all agents..."

for AGENT in $AGENTS; do
  INTENT_FILE="$INTENT_DIR/${AGENT}_intent.json"
  RESPONSE_FILE="$RESPONSE_DIR/${AGENT}_response.json"

  echo "{ \"check\": \"ping\", \"from\": \"corelight\", \"timestamp\": \"$(date)\" }" > "$INTENT_FILE"
done

sleep 3

for AGENT in $AGENTS; do
  RESPONSE_FILE="$RESPONSE_DIR/${AGENT}_response.json"
  if [ -f "$RESPONSE_FILE" ]; then
    echo "✅ $AGENT responded: $(cat $RESPONSE_FILE)" >> "$LOG"
  else
    echo "❌ $AGENT did not respond." >> "$LOG"
  fi
done

echo "🧠 Handshake complete. Check log: $LOG"
