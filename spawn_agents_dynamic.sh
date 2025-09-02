#!/bin/bash
echo "🌐 [InfinityXone] Dynamic Agent Spawner Activated"

INDEX_FILE="/opt/infinity_x_one/blueprints_index.txt"
BLUEPRINT_DIR="/opt/infinity_x_one/blueprints"
AGENTS_DIR="/opt/infinity_x_one/agents"
mkdir -p "$AGENTS_DIR"

if [ ! -f "$INDEX_FILE" ]; then
    echo "❌ Index file not found: $INDEX_FILE"
    exit 1
fi

while read -r line; do
    if [[ "$line" =~ ^[a-zA-Z0-9_-]+: ]]; then
        agent_name=$(echo "$line" | cut -d':' -f1)
        agent_file=$(echo "$line" | cut -d':' -f2- | xargs)
        target_dir="$AGENTS_DIR/$agent_name"

        echo "🧬 Spawning agent: $agent_name from $agent_file"
        mkdir -p "$target_dir"

        if [[ "$agent_file" == *.zip ]]; then
            unzip -o "$BLUEPRINT_DIR/$agent_file" -d "$target_dir"
        elif [[ "$agent_file" == *.ts || "$agent_file" == *.tsx || "$agent_file" == *.md || "$agent_file" == *.json || "$agent_file" == *.txt || "$agent_file" == *.docx ]]; then
            cp "$BLUEPRINT_DIR/$agent_file" "$target_dir/"
        else
            echo "⚠️ Unrecognized file type: $agent_file"
        fi
    fi
done < "$INDEX_FILE"

echo "✅ All agents deployed to: $AGENTS_DIR"
touch /opt/infinity_x_one/shared/heartbeat/DYNAMIC_SPAWN_COMPLETE.txt
