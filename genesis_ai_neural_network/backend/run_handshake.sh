#!/usr/bin/env bash
set -e
export PYTHONUNBUFFERED=1
# Primary
/opt/infinity_x_one/venv/bin/uvicorn backend.handshake_api:app --host 0.0.0.0 --port 8000 --workers 2 &
# Fallback
/opt/infinity_x_one/venv/bin/uvicorn backend.handshake_api:app --host 0.0.0.0 --port 8001 --workers 1 &
wait -n
