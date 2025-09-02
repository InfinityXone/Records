"""PickyBot worker.

PickyBot monitors efficiency metrics across the swarm and suggests
optimisations.  It reads data from `faucet_logs`, `profit_ledger` and
`swarm_state` and writes recommendations into Supabase.  This stub uses
random values to simulate performance and flags agents below a threshold.
"""

import random
import time
from typing import Dict

from ..supabase_utils import get_client, insert_log, fetch_pending_directives, mark_directive_complete

AGENT_NAME = "PickyBot"


def analyse_performance() -> Dict[str, float]:
    """Analyse agent performance and return a dict of agent → efficiency score."""
    client = get_client()
    # In a real implementation, compute scores based on logs and profits.
    agents = ["FaucetHunter", "KeyHarvester", "Atlas", "FinSynapse", "AnomalyHunter"]
    return {agent: random.uniform(0.5, 1.0) for agent in agents}


def suggest_actions(scores: Dict[str, float]) -> None:
    """Insert recommendations into Supabase based on performance scores."""
    for agent, score in scores.items():
        if score < 0.7:
            action = f"Scale up resources for {agent}" if score < 0.6 else f"Investigate {agent} performance"
            insert_log(
                "optimisation_actions",
                {"agent": AGENT_NAME, "target_agent": agent, "score": score, "action": action},
            )


def process_directive(directive: Dict) -> None:
    directive_id = directive["id"]
    command = directive["command"]
    if command == "ANALYSE_PERFORMANCE":
        scores = analyse_performance()
        suggest_actions(scores)
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "analysis_complete", "details": scores})
    else:
        insert_log("agent_logs", {"agent": AGENT_NAME, "event": "unknown_directive", "details": command})
    mark_directive_complete(directive_id)


def run_worker() -> None:
    while True:
        directives = fetch_pending_directives(AGENT_NAME)
        if directives:
            process_directive(directives[0])
        else:
            # Run performance analysis daily
            scores = analyse_performance()
            suggest_actions(scores)
            insert_log("agent_logs", {"agent": AGENT_NAME, "event": "heartbeat", "details": "performance analysis"})
            time.sleep(86400)


if __name__ == "__main__":
    run_worker()
