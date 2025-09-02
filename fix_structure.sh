#!/bin/bash
set -e

echo "[*] Stopping handshake_server..."
sudo systemctl stop handshake_server || true

echo "[*] Flattening directory..."
cd /opt/infinity_x_one/infinity-x-one

shopt -s dotglob
mv * ../

cd ..
rm -rf /opt/infinity_x_one/infinity-x-one

echo "[*] Updating systemd unit..."
sudo sed -i 's|/opt/infinity_x_one/infinity-x-one/|/opt/infinity_x_one/|g' /etc/systemd/system/handshake_server.service

echo "[*] Reloading systemd and restarting service..."
sudo systemctl daemon-reload
sudo systemctl restart handshake_server

echo "[*] Waiting 3s for service to boot..."
sleep 3

echo "[*] Checking port 8000..."
ss -tuln | grep 8000 || echo "⚠️ Port 8000 not active yet."

echo "[*] Checking logs..."
sudo tail -n 30 /opt/infinity_x_one/logs/handshake_server.log
