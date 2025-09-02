#!/bin/bash
set -e
echo "⚡ Bootstrapping Infinity X One Unified Neural Handshake..."

export SUPABASE_URL="https://xzxkyrdelmbqlcucmzpx.supabase.co"
export SUPABASE_SERVICE_KEY="YOUR_SERVICE_ROLE_KEY"

# Seed doctrine
python3 /opt/infinity_x_one/orchestrator/doctrine_loader.py

# Enable unified brain
cat <<EOF | sudo tee /etc/systemd/system/core_brain.service
[Unit]
Description=Infinity X One Unified Core Brain
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/core_brain.py
Restart=always
User=infinity-x-one
WorkingDirectory=/opt/infinity_x_one
Environment="SUPABASE_URL=$SUPABASE_URL"
Environment="SUPABASE_SERVICE_KEY=$SUPABASE_SERVICE_KEY"
StandardOutput=append:/var/log/core_brain.log
StandardError=append:/var/log/core_brain.log

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable core_brain
sudo systemctl restart core_brain

echo "✅ Neural Handshake complete. Core Brain running in background."
