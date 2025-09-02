#!/bin/bash
# guardian.sh – Trinity Protocol Layer 1: Ethical & Risk Sim Validation

AGENT_PATH="$2"
LOG_FILE="/opt/infinity_x_one/logs/guardian.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "[🛡️ Guardian] Simulating agent at: $AGENT_PATH" >> "$LOG_FILE"

# Simulate for known malicious or dangerous patterns
if grep -qE "rm\s+-rf|shutdown|format|:(){:|:&};:" "$AGENT_PATH"; then
    echo "[❌ Guardian] HIGH RISK action detected in $AGENT_PATH" >> "$LOG_FILE"
    exit 1
fi

# Scan for forbidden keywords
if grep -qi "override_security|unauthorized_access" "$AGENT_PATH"; then
    echo "[❌ Guardian] Unauthorized behavior found." >> "$LOG_FILE"
    exit 1
fi

echo "[✅ Guardian] Simulation passed for $AGENT_PATH" >> "$LOG_FILE"
exit 0
