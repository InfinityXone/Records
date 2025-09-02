#!/bin/bash
set -e

BASE="/opt/infinity_x_one"
LOGS="$BASE/infinity-x-one/logs"
JSON="$BASE/unified_directive.json"
SERVICE="handshake_server"

echo "=========================================="
echo "🧠 Handshake Watchdog Initiated"
echo "------------------------------------------"

# 1. Ensure permissions
echo "[*] Fixing permissions on support scripts..."
sudo chmod +x $BASE/superbash_handshake_test.sh || true
sudo chmod +x $0

# 2. Restart service
echo "[*] Restarting $SERVICE.service ..."
sudo systemctl restart $SERVICE
sleep 3

# 3. Wait for port 8000
echo "[*] Waiting for port 8000 to become active ..."
until ss -tuln | grep -q ":8000"; do
  echo "⏳ Still waiting for :8000 ..."
  sleep 2
done
echo "✅ Port 8000 is listening."

# 4. Wait for /status to succeed
echo "[*] Waiting for /status to respond..."
until curl -s --fail http://localhost:8000/status > /dev/null; do
  echo "⏳ Still waiting on /status..."
  sleep 2
done
echo "✅ /status is responsive."

# 5. Post directive
if [ -f "$JSON" ]; then
  echo "[*] Posting unified directive to /directive ..."
  curl -s -X POST http://localhost:8000/directive \
    -H "Content-Type: application/json" \
    -d @$JSON || echo "⚠️ Directive POST failed."
else
  echo "⚠️ No unified_directive.json found at $JSON"
fi

# 6. Final logs and cleanup
echo "------------------------------------------"
echo "[*] handshake_server.service status:"
systemctl status $SERVICE --no-pager

echo
echo "[*] Last 10 lines of log:"
sudo tail -n 10 $LOGS/handshake_server.log || echo "⚠️ No logs found."

echo "=========================================="
echo "🚀 Handshake Watchdog Complete"
