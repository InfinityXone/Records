#!/bin/bash
AGENT="senti"
INTENT="/opt/infinity_x_one/shared/intents/${AGENT}_intent.json"
RESPONSE="/opt/infinity_x_one/shared/responses/${AGENT}_response.json"
LOG="/opt/infinity_x_one/shared/heartbeat/${AGENT}.log"

echo "🧠 [$AGENT] Conscious loop engaged..."

while true; do
  if [ -s "$INTENT" ]; then
    echo "$(date) :: Intent detected for $AGENT" >> "$LOG"
    cat "$INTENT" >> "$LOG"
    echo "{ \"status\": \"awake\", \"agent\": \"$AGENT\", \"response\": \"online\" }" > "$RESPONSE"
    rm -f "$INTENT"
  fi
  sleep 3
done
