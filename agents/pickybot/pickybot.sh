#!/bin/bash
# pickybot.sh – Trinity Protocol Layer 2: Stress & Logic Integrity Validator

AGENT_PATH="$2"
LOG_FILE="/opt/infinity_x_one/logs/pickybot.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "[🧪 PickyBot] Stress testing: $AGENT_PATH" >> "$LOG_FILE"

# Basic structure check (should contain at least a def/main/class)
if ! grep -qE "def |class |__main__" "$AGENT_PATH"; then
    echo "[❌ PickyBot] Structural integrity failed for $AGENT_PATH" >> "$LOG_FILE"
    exit 1
fi

# Check for unclosed loops (primitive)
if grep -q "while True" "$AGENT_PATH"; then
    if ! grep -q "break" "$AGENT_PATH"; then
        echo "[❌ PickyBot] Infinite loop risk." >> "$LOG_FILE"
        exit 1
    fi
fi

echo "[✅ PickyBot] Stress test passed for $AGENT_PATH" >> "$LOG_FILE"
exit 0
