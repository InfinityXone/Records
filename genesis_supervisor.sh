#!/bin/bash
BASE="/opt/infinity_x_one"
SHARED="$BASE/shared"
while true; do
  for pid in $(pgrep -f core.sh); do
    if ! kill -0 $pid 2>/dev/null; then
      echo "⚠️ Restarting dead agent at $(date)" >> $SHARED/logs/supervisor.log
      bash $BASE/agents/*/core.sh &
    fi
  done
  sleep 10
done
