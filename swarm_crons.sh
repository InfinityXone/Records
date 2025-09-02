#!/bin/bash
# ==========================================================
# Infinity X One – Swarm Cron Job Setup
# Location: /opt/infinity_x_one/swarm_crons.sh
# Purpose:  Schedule 24/7 autonomous agent tasks
# ==========================================================

# Create log directory if missing
mkdir -p /var/log/infinity_x_one

# Write crontab entries
(crontab -l 2>/dev/null; cat <<'EOF'
# === Infinity X One Cron Jobs ===

# Faucet monitoring – every hour
0 * * * * /opt/infinity_x_one/agents/faucet_monitor.sh >> /var/log/infinity_x_one/faucet_monitor.log 2>&1

# Financial tracking – every 10 minutes
*/10 * * * * /opt/infinity_x_one/agents/fin_synapse_tracker.sh >> /var/log/infinity_x_one/fin_track.log 2>&1

# System health checks – every 30 minutes
*/30 * * * * /opt/infinity_x_one/agents/guardian_healthcheck.sh >> /var/log/infinity_x_one/guardian.log 2>&1

# Agent performance evaluation – every 4 hours
0 */4 * * * /opt/infinity_x_one/agents/pickybot_audit.sh >> /var/log/infinity_x_one/pickybot.log 2>&1

# === End Infinity X One Cron Jobs ===
EOF
) | crontab -
