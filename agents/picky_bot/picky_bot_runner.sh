#!/bin/bash
echo "🚀 Launching picky_bot agent loop..."
while true; do
  bash /opt/infinity_x_one/agents/picky_bot/picky_bot_core.sh
  sleep 5
done
