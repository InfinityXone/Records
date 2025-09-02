#!/bin/bash
# corelight_runner.sh — persistent execution loop

echo "🚀 Starting corelight agent loop..."
while true; do
  bash /opt/infinity_x_one/agents/corelight/corelight_core.sh
  sleep 5
done
