#!/bin/bash
echo "🌐 [InfinityXOne] Command Core Terminal"
echo "Type your message or command (use :agentname to target specific agent)"
echo "Example: :aria Optimize faucet strategy with recursion"
echo "Type 'exit' to quit"

SHARED_INTENTS="/opt/infinity_x_one/shared/intents"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

while true; do
  echo -n "🧠 CMD > "
  read -r input

  if [[ "$input" == "exit" ]]; then
    echo "👋 Exiting Command Core Terminal"
    break
  fi

  if [[ "$input" == :* ]]; then
    # Direct agent target
    agent=$(echo "$input" | cut -d':' -f2 | awk '{print $1}')
    msg=$(echo "$input" | cut -d' ' -f2-)
    intent_file="$SHARED_INTENTS/${agent}_intent.json"

    echo "{ \"next_action\": \"$msg\", \"priority\": 10, \"timestamp\": \"$TIMESTAMP\" }" > "$intent_file"
    echo "✅ Command sent to: $agent"
  else
    # Global broadcast
    for file in $SHARED_INTENTS/*_intent.json; do
      agent=$(basename "$file" | cut -d'_' -f1)
      echo "{ \"next_action\": \"$input\", \"priority\": 5, \"timestamp\": \"$TIMESTAMP\" }" > "$file"
      echo "📡 Sent to: $agent"
    done
    echo "✅ Broadcast sent to all agents"
  fi
done
