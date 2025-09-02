#!/bin/bash

SHARED="/opt/infinity_x_one/shared/intents"
AGENTS=(corelight aria lumi senti vita anima codex echo fin_synapse guardian infinity_agent_one picky_bot vision)

mkdir -p "$SHARED"

for AGENT in "${AGENTS[@]}"; do
  INTENT_FILE="$SHARED/${AGENT}_intent.json"
  if [ ! -f "$INTENT_FILE" ]; then
    touch "$INTENT_FILE"
    echo "🪄 Created empty intent for $AGENT"
  else
    echo "✔️ Intent already exists for $AGENT"
  fi
done

