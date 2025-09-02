#!/bin/bash
set -e
BASE="/opt/infinity_x_one/infinity-x-one"
LOGS="$BASE/logs"
JSON="/opt/infinity_x_one/unified_directive.json"

echo "===================================================="
echo "[*] Checking port 8000 ..."
if ss -tuln | grep -q ":8000"; then
  echo "✅ Port 8000 is listening."
else
  echo "⚠️ Port 8000 not found listening."
fi

echo
echo "[*] Last 20 log lines from handshake_server.log ..."
tail -n 20 $LOGS/handshake_server.log || echo "⚠️ No log file yet."

echo
echo "[*] Checking /status endpoint ..."
curl -s http://localhost:8000/status || echo "⚠️ Status endpoint failed."

if [ -f "$JSON" ]; then
  echo
  echo "[*] Posting unified directive to /directive ..."
  curl -s -X POST http://localhost:8000/directive \
    -H "Content-Type: application/json" \
    -d @$JSON || echo "⚠️ Directive POST failed."
else
  echo "⚠️ No unified_directive.json found at $JSON"
fi

echo
echo "===================================================="
echo "✅ Handshake test complete."
echo "Check above for /status output and directive response."
