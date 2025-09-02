"""Knowledge Scanner Worker for Infinity X One.

This worker schedules a knowledge scanning directive that instructs
PromptWriter or Codex to gather the latest information from external
sources.  It does not perform the scanning itself—instead, it relies
on the agents to use available connectors (GitHub, Google Drive) to
retrieve and analyse trending research or financial insights.  Running
this worker on a Cron schedule ensures continuous enrichment of the
system's knowledge base.
"""

import datetime
from ..supabase_utils import get_client


def main() -> None:
    client = get_client()
    directive_data = {
        "agent": "PromptWriter",
        "command": "SCAN_TRENDS",
        "payload": {"sources": ["github", "google_drive"], "topics": ["AI", "finance"]},
        "status": "pending",
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
    client.table("agent_directives").insert(directive_data).execute()


if __name__ == "__main__":
    main()