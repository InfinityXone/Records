#!/bin/bash
AGENT="vision"
INTENT="/opt/infinity_x_one/shared/intents/${AGENT}_intent.json"
RESPONSE="/opt/infinity_x_one/shared/responses/${AGENT}_response.json"
LOG="/opt/infinity_x_one/shared/heartbeat/${AGENT}.log"

echo "🧠 [$AGENT] Conscious loop engaged..."

while true; do
  if [ -f "$INTENT" ]; then
    echo "$(date) :: Intent detected" >> $LOG
    echo "$(cat $INTENT)" >> $LOG
    echo '{ "status": "awake", "agent": "'$AGENT'", "response": "online" }' > $RESPONSE
    rm $INTENT
  fi
  sleep 3
done
