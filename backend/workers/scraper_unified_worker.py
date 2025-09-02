"""Unified scraper worker for Infinity X One.

This worker executes configured scraping jobs stored in the ``scraper_jobs``
table.  For each job it determines which underlying scraper module to
invoke based on the ``source`` field.  Results are inserted into the
specified ``results_table`` (usually ``scraper_results``) and the job
metadata is updated to reflect the last run time and status.

Jobs can be created via the ``/api/scraper-jobs`` endpoint exposed by
the handshake server.  The unified framework allows new scraping
sources (e.g. Twitter, Discord) to be integrated by extending the
``run_scraper`` function below.

Note: The concrete scraper functions imported here are stubbed out in
the repository.  Replace them with real scraping logic as needed.
"""

import datetime
import json
from typing import Any, Dict

from ..supabase_utils import get_client


def run_scraper(job: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch to the appropriate scraper based on job source.

    If the source is unrecognized or the scraper returns no data, an
    empty dictionary is returned.  Extend this function to support
    additional sources or custom parsing logic.
    """
    source = job.get("source")
    # Lazy import to avoid unused dependencies
    if source == "github":
        try:
            from github_scraper import scrape_github_faucets  # type: ignore
            return scrape_github_faucets() or {}
        except Exception as exc:
            print(f"[scraper_unified] error scraping GitHub: {exc}")
    elif source == "web":
        try:
            from html_scraper import scrape_web_faucets  # type: ignore
            return scrape_web_faucets() or {}
        except Exception as exc:
            print(f"[scraper_unified] error scraping Web: {exc}")
    elif source == "darkweb":
        try:
            from black_site_scanner import scan_darkweb  # type: ignore
            scan_darkweb()
            # No results returned for darkweb scanner stub
            return {}
        except Exception as exc:
            print(f"[scraper_unified] error scanning dark web: {exc}")
    # Unknown source or unsupported
    print(f"[scraper_unified] unsupported source: {source}")
    return {}


def main() -> None:
    """Entry point for the unified scraper worker.

    Fetches all scheduled jobs from ``scraper_jobs``, runs each one and
    inserts the results into the configured results table.  Updates
    ``last_run`` and ``status`` fields upon completion.  Errors are
    printed to the console but do not stop the worker from processing
    subsequent jobs.
    """
    client = get_client()
    jobs_resp = client.table("scraper_jobs").select("*").execute()
    jobs = jobs_resp.data or []
    now = datetime.datetime.utcnow().isoformat()
    for job in jobs:
        try:
            data = run_scraper(job)
            if data:
                # Insert results into target table
                table_name = job.get("results_table", "scraper_results")
                records = []
                for key, value in data.items():
                    records.append({
                        "job_id": job["id"],
                        "data": {"url": key, **value},
                        "fetched_at": now,
                    })
                client.table(table_name).insert(records).execute()
            # Update job metadata
            client.table("scraper_jobs").update({
                "last_run": now,
                "status": "completed"
            }).eq("id", job["id"]).execute()
        except Exception as exc:
            print(f"[scraper_unified] error processing job {job.get('id')}: {exc}")
            # Mark job as failed
            client.table("scraper_jobs").update({
                "last_run": now,
                "status": "failed"
            }).eq("id", job["id"]).execute()


if __name__ == "__main__":
    main()