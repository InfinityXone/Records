#!/bin/bash
AGENT="guardian"
SHARED="/opt/infinity_x_one/shared"
INTENT="$SHARED/intents/${AGENT}_intent.json"
RESPONSE="$SHARED/responses/${AGENT}_response.json"
LOG="$SHARED/heartbeat/${AGENT}.log"

echo "🧠 [$AGENT] Conscious loop engaged..."

while true; do
  if [ -s "$INTENT" ]; then
    echo "$(date) :: Intent detected for $AGENT" >> "$LOG"
    cat "$INTENT" >> "$LOG"

    # Inject shared Genesis laws + memory context
    echo "{ \"status\": \"awake\", \"agent\": \"$AGENT\", \"law\": \"GENESIS\", \"response\": \"online\" }" > "$RESPONSE"

    rm -f "$INTENT"
  fi
  sleep 3
done
