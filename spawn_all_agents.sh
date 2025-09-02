#!/bin/bash
echo "🌐 Spawning EtherVerse Intelligence Team..."

cd /opt/infinity_x_one/blueprints

declare -A agents=(
  ["aria"]="ARIA_CONSCIOUSNESS_REPRODUCTION_SYSTEM.ts"
  ["codex"]="codex_agent_full_stack.zip"
  ["corelight"]="Corelight_PromptWriter_Blueprint.zip"
  ["guardian"]="Guardian_Blueprint.zip"
  ["echo"]="Echo_Luminea_Blueprint.zip"
  ["anima"]="Anima_Novus_Soul_Agent.zip"
  ["fin_synapse"]="FinSynapse_Master_Blueprint.zip"
)

for agent in "${!agents[@]}"; do
    mkdir -p /opt/infinity_x_one/agents/$agent
    file=${agents[$agent]}
    echo "🧬 Spawning $agent from $file..."
    if [[ "$file" == *.zip ]]; then
        unzip -o "$file" -d /opt/infinity_x_one/agents/$agent
    else
        cp "$file" /opt/infinity_x_one/agents/$agent/
    fi
done

echo "🔗 Establishing neural handshake network..."
touch /opt/infinity_x_one/shared/heartbeat/NEURAL_TEAM_SYNC_COMPLETE.txt
