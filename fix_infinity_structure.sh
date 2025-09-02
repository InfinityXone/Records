#!/bin/bash
set -e

echo "[*] Cleaning nested /infinity-x-one directory..."

# Move logs up if they exist
if [ -d "/opt/infinity_x_one/infinity-x-one/logs" ]; then
    echo "[*] Moving logs to correct location..."
    sudo mv /opt/infinity_x_one/infinity-x-one/logs/* /opt/infinity_x_one/logs/ || true
fi

# Remove the incorrect nested directory
sudo rm -rf /opt/infinity_x_one/infinity-x-one
echo "[+] Removed /opt/infinity_x_one/infinity-x-one"

# Fix systemd unit if needed
SERVICE_FILE="/etc/systemd/system/handshake_server.service"
if grep -q "infinity-x-one" "$SERVICE_FILE"; then
    echo "[*] Fixing systemd ExecStart path..."

    sudo sed -i 's|/opt/infinity_x_one/infinity-x-one/core/handshake_server.py|/opt/infinity_x_one/core/handshake_server.py|g' $SERVICE_FILE
    sudo sed -i 's|WorkingDirectory=/opt/infinity_x_one/infinity-x-one/core|WorkingDirectory=/opt/infinity_x_one/core|g' $SERVICE_FILE
fi

# Reload systemd and restart
echo "[*] Reloading systemd daemon and restarting handshake_server..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart handshake_server.service

# Confirm port 8000
echo "[*] Waiting for port 8000 to open..."
for i in {1..20}; do
    sleep 1
    if ss -tuln | grep -q ':8000'; then
        echo "✅ Port 8000 is active!"
        break
    fi
    echo "⏳ Waiting for port 8000..."
done

# Final status check
echo "===================================================="
sudo systemctl status handshake_server --no-pager
ss -tuln | grep 8000 || echo "❌ Port 8000 not active"
echo "===================================================="
