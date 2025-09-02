#!/bin/bash
set -e
BASE="/opt/infinity_x_one/infinity-x-one"
CORE="$BASE/core"
LOGS="$BASE/logs"

echo "[*] Installing handshake_server.service ..."

cat > /etc/systemd/system/handshake_server.service <<SERVICE
[Unit]
Description=Infinity X One Handshake Server
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/python $CORE/handshake_server.py
WorkingDirectory=$CORE
Restart=always
StandardOutput=append:$LOGS/handshake_server.log
StandardError=append:$LOGS/handshake_server.err

[Install]
WantedBy=multi-user.target
SERVICE

echo "[*] Reloading systemd and enabling service ..."
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable handshake_server
systemctl restart handshake_server

echo "[*] Checking status ..."
systemctl status handshake_server --no-pager

echo "[*] Verifying port 8000 ..."
ss -tuln | grep 8000 || echo "⚠️ Nothing listening on port 8000 yet!"

echo "===================================================="
echo "✅ handshake_server.service installed and restarted"
echo "✅ Logs: $LOGS/handshake_server.log"
echo "===================================================="
echo "Next step: run your unified_directive.json POST again:"
echo "curl -X POST http://localhost:8000/directive -H 'Content-Type: application/json' -d @/opt/infinity_x_one/unified_directive.json"
