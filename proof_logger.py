#!/usr/bin/env python3
import logging
logging.basicConfig(filename="~/logs/proof_logger.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.info("Starting proof_logger.py")
import json
from datetime import datetime

def log_proof(agent_id, task_name, status):
    log_entry = {
        "agent": agent_id,
        "task": task_name,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    try:
        with open("proof_log.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data.append(log_entry)
    with open("proof_log.json", "w") as f:
        json.dump(data, f, indent=2)
