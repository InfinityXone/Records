#!/bin/bash
echo "🔍 Verifying Neural Handshake & Agent Autonomy..."

# Correct Supabase transaction pooler connection string (IPv4-compatible, us-east-2, port 6543)
SUPABASE_CONN="postgresql://postgres.xzxkyrdelmbqlcucmzpx:Jasontb1234!!@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

# Check oath commitments
psql "$SUPABASE_CONN" -c "SELECT agent_name, status, created_at FROM oath_commitments ORDER BY created_at DESC LIMIT 10;"

# Check handshake event
psql "$SUPABASE_CONN" -c "SELECT actor, subject, decision, reason, ts FROM integrity_events ORDER BY ts DESC LIMIT 5;"

# Check agent directives
psql "$SUPABASE_CONN" -c "SELECT agent, command, status, priority FROM agent_directives ORDER BY created_at DESC LIMIT 20;"

# Check agent logs
psql "$SUPABASE_CONN" -c "SELECT log_time, level, message FROM agent_logs ORDER BY log_time DESC LIMIT 10;"

# Check reports
psql "$SUPABASE_CONN" -c "SELECT timestamp, swarm_log, financial FROM reports_live ORDER BY timestamp DESC LIMIT 5;"

