"""Worker package for Infinity X One.

Each module in this package defines a long‑running process that polls
Supabase for directives targeted at a specific agent.  When a directive
arrives, the worker executes the requested command and logs the result.

To launch a worker locally, run the module as a script, for example:

```bash
python3 -m deployment_package.backend.workers.faucet_worker
```
"""
