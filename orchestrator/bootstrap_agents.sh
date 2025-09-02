#!/bin/bash
# 🚀 Bootstrap: AtlasBot + KeyHarvester Agents
# This script sets up blueprints and registers both agents under Neural Handshake

echo "🧬 Initializing AtlasBot + KeyHarvester..."

# 1. Register AtlasBot directive
curl -s http://localhost:8000/directive -X POST -H "Content-Type: application/json" -d '{
  "protocol":"NeoPulse-2025-001",
  "agent":"Codex",
  "command":"DeployAtlasBot",
  "priority":5,
  "payload":{
    "blueprint":"atlas_bot.py",
    "source":"Atlas Bot Creator Prompt",
    "objectives":[
      "Automate account signup (AWS, GCP, Vast.ai, RunPod)",
      "Store credentials in Supabase key_vault",
      "Provision nodes via API",
      "Register nodes into swarm_state"
    ],
    "supporting_agents":{
      "Guardian":"identity rotation + waste prevention",
      "PickyBot":"audit uptime/cost/profit",
      "Infinity Agent One":"connect new nodes into swarm"
    }
  }
}'

# 2. Register KeyHarvester directive
curl -s http://localhost:8000/directive -X POST -H "Content-Type: application/json" -d '{
  "protocol":"NeoPulse-2025-001",
  "agent":"Codex",
  "command":"DeployKeyHarvester",
  "priority":5,
  "payload":{
    "blueprint":"api_key_harvester.ts",
    "source":"API_KEY_HARVESTING_AGENT_SYSTEM",
    "objectives":[
      "Continuously scan for expired/unused API keys",
      "Rotate keys on schedule",
      "Insert keys into Supabase key_vault",
      "Expose keys securely to active agents"
    ],
    "supporting_agents":{
      "Guardian":"monitor misuse/abuse",
      "PromptWriter":"document rotations",
      "Echo":"log activity to agent_logs"
    }
  }
}'

# 3. Confirmation
echo "✅ AtlasBot + KeyHarvester blueprints registered. Supabase will track directives, Guardian & Picky enforce safety/quota."
