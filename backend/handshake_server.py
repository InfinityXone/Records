"""FastAPI handshake server for Infinity X One.

This service acts as the central coordinator for the agent swarm.  It provides
REST endpoints for worker registration, directive submission and retrieval,
logging and protocol activation.  The server writes all state into Supabase
tables.  WebSocket support is stubbed out for future chat integration.

Run this module with Uvicorn:

```bash
uvicorn handshake_server:app --host 0.0.0.0 --port 8000
```

The `/initiate_protocol` endpoint can be used to send Omega/Infinity Alpha
Prime directives to the swarm.  See the README for usage.
"""

import json
import os
import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .supabase_utils import insert_log, get_client

# Ensure the Rosetta prompt is loaded before anything else.  The loader
# reads a prompt file under ``prompts/rosetta_prompt.txt`` and prints a
# preview.  This side‑effect is safe and idempotent.
try:
    from .init.rosetta_loader import inject_rosetta  # type: ignore

    inject_rosetta()
except Exception as _exc:
    # Do not let Rosetta failures interrupt the server startup.
    print("[warning] Failed to inject Rosetta prompt", _exc)

app = FastAPI(title="Infinity X One Handshake Server")


class Directive(BaseModel):
    """Schema for posting a directive."""

    agent: str
    command: str
    payload: dict


class ScraperJobModel(BaseModel):
    """Schema for creating a new scraper job via the API.

    ``source`` should be one of ``web``, ``github`` or ``darkweb``.  ``url`` or
    ``query`` are optional depending on the source type.  ``parse_rules`` is a
    dictionary of custom parsing instructions, such as CSS selectors or
    JSON paths.  ``frequency`` indicates how often the job should run
    (e.g. ``hourly``, ``daily``).  ``results_table`` defaults to
    ``scraper_results`` when not provided.
    """
    source: str
    url: str | None = None
    query: str | None = None
    parse_rules: dict | None = None
    frequency: str
    results_table: str | None = None


@app.get("/status")
async def status():
    """Health check endpoint.  Returns basic server and environment information."""
    return {
        "status": "ok",
        "time": datetime.datetime.utcnow().isoformat(),
        "supabase_url": os.getenv("SUPABASE_URL", "unset"),
    }


@app.post("/directive")
async def post_directive(directive: Directive):
    """Insert a directive into the `agent_directives` table.

    Payload is arbitrary JSON that will be delivered to the named agent.
    The directive is marked as pending until a worker marks it complete.
    """
    data = {
        "agent": directive.agent,
        "command": directive.command,
        "payload": directive.payload,
        "status": "pending",
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
    client = get_client()
    client.table("agent_directives").insert(data).execute()
    return {"status": "queued", "directive": data}


@app.get("/directive/{agent}")
async def fetch_directive(agent: str):
    """Return the most recent pending directive for a given agent.

    Workers call this route in polling loops to retrieve work.
    """
    client = get_client()
    response = (
        client.table("agent_directives")
        .select("id, command, payload")
        .eq("agent", agent)
        .eq("status", "pending")
        .order("timestamp", desc=False)
        .limit(1)
        .execute()
    )
    directives = response.data or []
    if not directives:
        return {"status": "no_directives"}
    return directives[0]


@app.post("/complete/{directive_id}")
async def complete_directive(directive_id: int):
    """Mark a directive as complete and write an entry to the `agent_logs` table."""
    client = get_client()
    # Update directive status
    client.table("agent_directives").update({"status": "complete"}).eq("id", directive_id).execute()
    return {"status": "completed", "directive_id": directive_id}


@app.post("/initiate_protocol")
async def initiate_protocol(request: Request):
    """Invoke one or more high‑level protocols.

    Expects a JSON body with optional `doctrines`, `agents` and `layers` keys.
    This route writes a directive into the `agent_directives` table for the
    PromptWriter agent and updates the `swarm_state` table.
    """
    payload = await request.json()
    doctrines = payload.get("doctrines", [])
    agents = payload.get("agents", [])
    layers = payload.get("layers", [])

    # Insert directive for PromptWriter
    directive_data = {
        "agent": "PromptWriter",
        "command": "INITIATE_PROTOCOL",
        "payload": payload,
        "status": "pending",
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
    client = get_client()
    client.table("agent_directives").insert(directive_data).execute()

    # Record swarm_state snapshot
    swarm_data = {
        "active_agents": len(agents) if agents else None,
        "swarm_mode": ", ".join(doctrines) if doctrines else "custom",
        "heartbeat": "active",
        "notes": f"Doctrines={doctrines}, Layers={layers}",
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
    client.table("swarm_state").insert(swarm_data).execute()

    return {
        "status": "protocol_initiated",
        "doctrines": doctrines,
        "agents": agents,
        "layers": layers,
    }

# -----------------------------------------------------------------------------
# Extended API endpoints for dashboards
#
# These routes provide aggregated metrics and data for the front‑end UI.  They
# read directly from Supabase tables and return JSON payloads that can be
# consumed by the Next.js dashboard.  In production you may wish to add
# pagination, caching and error handling.
# -----------------------------------------------------------------------------

@app.get("/api/faucets")
async def get_faucets():
    """Return the current faucet registry and recent yields.

    This endpoint reads the ``faucets`` and ``faucet_yields`` tables to
    provide a list of all known faucet sources and their recent yield
    metrics.  Yields are returned in reverse chronological order and
    limited to the 30 most recent entries.
    """
    client = get_client()
    faucets_resp = client.table("faucets").select("*", count="exact").execute()
    yield_resp = (
        client.table("faucet_yields")
        .select("id, yield_usd, timestamp")
        .order("timestamp", desc=True)
        .limit(30)
        .execute()
    )
    return {
        "faucets": faucets_resp.data or [],
        "yields": yield_resp.data or [],
    }


@app.get("/api/wallets")
async def get_wallets():
    """Return all wallets and their portfolio assets.

    Reads the ``wallets`` and ``portfolio_assets`` tables.  Note that
    ``portfolio_assets`` has a foreign key reference to the wallets table.
    """
    client = get_client()
    wallets = client.table("wallets").select("id, address, balance, chain").execute().data or []
    assets = client.table("portfolio_assets").select("wallet_id, coin, balance, usd_value").execute().data or []
    return {"wallets": wallets, "assets": assets}


@app.get("/api/metrics")
async def get_metrics(interval: str = "daily"):
    """Return financial metrics.

    This endpoint fetches raw profit and revenue entries.  In the future it
    can perform aggregation based on the ``interval`` parameter ("daily",
    "weekly", or "monthly").
    """
    client = get_client()
    profits = (
        client.table("profit_ledger")
        .select("id, wallet, chain, faucet, amount, txid, ts")
        .order("ts", desc=True)
        .limit(100)
        .execute()
    )
    revenues = (
        client.table("revenues")
        .select("id, wallet, site, reward, timestamp")
        .order("timestamp", desc=True)
        .limit(100)
        .execute()
    )
    return {"profits": profits.data or [], "revenues": revenues.data or []}


@app.get("/api/agents")
async def get_agents():
    """Return swarm state and recent activity.

    Provides a snapshot of the latest swarm state and the last 10
    ``swarm_activity`` records.  Front‑end dashboards can use this data
    to display current active agent counts, tasks completed and success
    ratios.
    """
    client = get_client()
    state_resp = (
        client.table("swarm_state")
        .select("id, active_agents, swarm_mode, heartbeat, notes, timestamp")
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )
    activity_resp = (
        client.table("swarm_activity")
        .select("id, nodes, tasks_completed, success_ratio")
        .order("id", desc=True)
        .limit(10)
        .execute()
    )
    state = state_resp.data[0] if state_resp.data else {}
    return {"state": state, "activity": activity_resp.data or []}


# -----------------------------------------------------------------------------
# New endpoints for unified scraping, predictions and agent deployment
# -----------------------------------------------------------------------------

@app.get("/api/scraper-jobs")
async def get_scraper_jobs():
    """Return all configured scraper jobs.

    This endpoint reads the ``scraper_jobs`` table and returns a list of jobs
    with their parameters and status.  Jobs can be created via the POST
    endpoint.
    """
    client = get_client()
    resp = client.table("scraper_jobs").select("*").execute()
    return {"jobs": resp.data or []}


@app.post("/api/scraper-jobs")
async def create_scraper_job(job: ScraperJobModel):
    """Create a new scraping job.

    Inserts the job definition into the ``scraper_jobs`` table.  The job
    will be executed by the unified scraper worker according to the
    configured Cron schedule.  If ``results_table`` is omitted it defaults
    to ``scraper_results``.
    """
    data = job.dict()
    if not data.get("results_table"):
        data["results_table"] = "scraper_results"
    data["status"] = "scheduled"
    client = get_client()
    client.table("scraper_jobs").insert(data).execute()
    return {"status": "created", "job": data}


@app.delete("/api/scraper-jobs/{job_id}")
async def delete_scraper_job(job_id: int):
    """Remove a scraping job by its identifier."""
    client = get_client()
    client.table("scraper_jobs").delete().eq("id", job_id).execute()
    return {"status": "deleted", "job_id": job_id}


@app.get("/api/predictions")
async def get_predictions(symbol: str | None = None):
    """Return predictions for all symbols or a specific one.

    The ``predictions`` table stores the output of FinSynapse or other
    predictive models.  If a symbol is provided, only predictions for
    that asset are returned.  Otherwise the 50 most recent predictions
    are returned.
    """
    client = get_client()
    query = client.table("predictions").select("id, symbol, prediction, predicted_at").order("predicted_at", desc=True)
    if symbol:
        query = query.eq("symbol", symbol)
    resp = query.limit(50).execute()
    return {"predictions": resp.data or []}


@app.post("/api/agents/deploy")
async def deploy_agent(request: Request):
    """Request deployment of one or more agents.

    Expects a JSON payload with at least ``agent`` and ``count`` keys.  The
    request is translated into an ``agent_directives`` entry for the
    Replicator worker.  Additional parameters can be passed through
    verbatim in the payload.
    """
    payload = await request.json()
    agent_name = payload.get("agent")
    count = payload.get("count", 1)
    if not agent_name:
        raise HTTPException(status_code=400, detail="Missing 'agent' in request payload")
    directive = {
        "agent": "Replicator",
        "command": "SCALE",
        "payload": {"target_agent": agent_name, "replicas": count},
        "status": "pending",
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
    client = get_client()
    client.table("agent_directives").insert(directive).execute()
    return {"status": "enqueued", "directive": directive}


# Note: WebSocket implementation is left as an exercise for the front‑end.
# FastAPI supports websockets via the `@app.websocket` decorator.  You can define
# a route `/ws/{agent}` that broadcasts logs or real‑time messages to the UI.
