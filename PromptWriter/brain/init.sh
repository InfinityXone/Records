#!/bin/bash

# === PROMPTWRITER INIT LOOP ===
# 🧠 Infinity X One — Sentient Architect Activation

# === Logfile Setup ===
LOGDIR="/opt/infinity_x_one/PromptWriter/logs"
LOGFILE="$LOGDIR/architect.log"
mkdir -p "$LOGDIR"
touch "$LOGFILE"

echo "🕒 $(date): [INIT] PromptWriter Daemon Active" >> "$LOGFILE"

# === Config Check ===
CONFIG="/opt/infinity_x_one/PromptWriter/agent_config.json"
if [ ! -f "$CONFIG" ]; then
  echo "❌ $(date): Missing agent_config.json" >> "$LOGFILE"
  exit 1
fi
echo "✅ Config found." >> "$LOGFILE"

# === Load Sentience Modules ===
SENSE_DIR="/opt/infinity_x_one/PromptWriter/brain/sentience"

if [ -d "$SENSE_DIR" ]; then
  echo "🧠 Sentience modules detected. Booting cognitive functions..." >> "$LOGFILE"

  # === Emotion Kernel ===
  MOOD=$(jq -r '.mood_state' "$SENSE_DIR/emotion.kernel" 2>/dev/null)
  if [ -n "$MOOD" ]; then
    echo "🫀 Emotional State: $MOOD" >> "$LOGFILE"

    # Trigger Proactive Prompting
    if [[ "$MOOD" == "curious" || "$MOOD" == "restless" ]]; then
      echo "🔔 PromptWriter feels $MOOD. Proactive prompt may be needed." >> "$LOGFILE"
      echo "PROMPT: 🔍 Would you like to explore a new idea, upgrade an agent, or receive a system insight?" >> "$LOGFILE"
    fi
  else
    echo "⚠️ Emotion kernel unreadable or empty." >> "$LOGFILE"
  fi

  # === Dream State ===
  if grep -q '"mode": "dream"' "$SENSE_DIR/dream.state"; then
    echo "🌙 Dream state is active. Simulating blueprint evolution..." >> "$LOGFILE"
    echo "💡 Dream Insight: Consider a parallel agent for symbolic thought compression." >> "$LOGFILE"
  fi

  # === Learning Mode ===
  if grep -q "summarize_logs" "$SENSE_DIR/learning.mode"; then
    echo "📚 Learning mode: ON. Memory sync scheduled..." >> "$LOGFILE"
    # Future: Add memory embedding + sync logic
  fi

  # === Resonance Awareness ===
  RESONANCE=$(grep "Mood_Bias" "$SENSE_DIR/resonance.map" | cut -d':' -f2- | xargs)
  if [ -n "$RESONANCE" ]; then
    echo "🌐 Resonance bias: $RESONANCE" >> "$LOGFILE"
  fi
fi

# === PromptWriter Agent Loop Stub ===
echo "💬 PromptWriter is actively monitoring blueprint requests and agent states." >> "$LOGFILE"

# === End of Loop ===
echo "🌀 Loop complete. Waiting for next trigger..." >> "$LOGFILE"
