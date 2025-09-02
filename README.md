# Infinity X One — Production‑Grade Faucet, Drip & Airdrop System

This directory contains a **self‑contained deployment package** for the Infinity X One agentic swarm.  It provides all of the code, configuration, and manifests needed to run a fully autonomous crypto‑faucet/airdrop/drip ecosystem on a Kubernetes cluster.  The design follows the user’s 30‑day growth plan and 6‑month scale strategy.

## Components overview

### 🧠 Backend

The backend is comprised of a **FastAPI handshake server** and a set of **worker agents**, each responsible for a different task in the swarm:

| Component | Purpose |
|---|---|
| `handshake_server.py` | Exposes REST/WebSocket endpoints used by the front‑end and other agents.  Supports the `/initiate_protocol` route for Omega + Infinity Alpha Prime activation.  Logs directives to Supabase and updates the `swarm_state` table. |
| `supabase_utils.py` | Helper for connecting to Supabase using environment variables.  Provides simple `insert_log`, `get_directives` and other convenience functions. |
| `workers/faucet_worker.py` | Polls the **Top 200 Crypto Faucets** list and dispatches claim tasks.  Records results into the `faucet_logs` and `profit_ledger` tables.  Designed to scale out via K8s replicas. |
| `workers/key_harvester.py` | Harvests free API keys, API tokens and trial credits from providers (Moralis, Infura, etc.).  Stores them in Supabase for other agents. |
| `workers/atlas_worker.py` | Handles compute provisioning.  It stubs out API calls to cloud providers (AWS, GCP, RunPod, Vast.ai) and writes available node credentials into Supabase.  In a real deployment, you would implement the provider APIs here. |
| `workers/replicator_worker.py` | Uses `agent_replicator.map.json` and `planetary.*.json` to spawn additional copies of Infinity Agent One and other modules across the cluster.  It keeps a log of replication events in Supabase. |
| `workers/anomaly_worker.py` | Scans for hidden crypto anomalies and potential arbitrage opportunities.  Currently calls a stubbed function from `HIDDEN_CRYPTO_ANOMALIES_SYSTEM (2).ts` but can be extended. |
| `workers/wallet_monitor.py` | Monitors the user’s Ethereum and Solana wallets for balance changes and airdrop deposits.  Uses the keys from the “keys‑to‑the‑house” file (environment variables). |
| `workers/fin_synapse_worker.py` | Coordinates yield farming and staking via FinSynapse.  This worker reads profits from `profit_ledger` and optionally interacts with the **Infinity Coin** smart contract.  If the contract is not deployed on a public chain, it logs reward events into Supabase. |
| `workers/guardian_worker.py` | Security and integrity watchdog.  Runs periodic checks on agent logs and enforces the oath.  Writes to `integrity_events`. |
| `workers/pickybot_worker.py` | Efficiency auditor.  Tracks performance of faucet claims and flags underperforming agents for scaling decisions.  Writes to `swarm_state`. |
| `workers/promptwriter_worker.py` | Meta‑architect.  Reads high‑level directives (e.g. “Infinity Alpha Prime Protocol”) from Supabase and orchestrates other workers accordingly. |
| `workers/codex_worker.py` | System builder and deployment coordinator.  Compiles new scripts, writes Kubernetes manifests, and can push changes to GitHub. |

### 🗄️ Supabase schema

You should run the migration contained in `migrations/omega_schema_patch.sql` against your Supabase instance.  It creates indexes and foreign keys on high‑traffic tables such as `agent_logs`, `profit_ledger`, `faucet_logs`, and ensures referential integrity for `wallets` and `profit_ledger`.

### ☸️ Kubernetes manifests

Manifests in the `k8s/` folder describe how to deploy the system onto a Kubernetes cluster.  Highlights:

* **`handshake-server.yaml`** – Deploys the FastAPI handshake server with two replicas, exposes ports 8000 and 8001 and mounts environment variables from a Kubernetes secret.
* **`workers.yaml`** – A collection of `Deployment` objects, one per worker.  Each uses a light Python image and points at the corresponding script under `backend/workers/`.  You can adjust the `replicas` count to scale any worker.  The Infinity Agent One replicator is automatically scaled via a Horizontal Pod Autoscaler (HPA) defined in this file.
* **`cronjobs.yaml`** – Defines Kubernetes `CronJob` resources for periodic tasks such as faucet harvest checks, anomaly scans and guardian audits.  These run on a schedule instead of as long‑lived deployments.

Before applying the manifests, create a Kubernetes secret named `infinity-env` containing the contents of your `INFINITY X ONE MASTER ENV.txt` file:

```bash
kubectl create secret generic infinity-env \
  --from-env-file=/path/to/INFINITY\ X\ ONE\ MASTER\ ENV.txt
```

Then apply the manifests:

```bash
kubectl apply -f k8s/handshake-server.yaml
kubectl apply -f k8s/workers.yaml
kubectl apply -f k8s/cronjobs.yaml
```

### 💻 Front‑end

The `frontend/` directory contains a **Next.js + Tailwind** skeleton for the AgentGPT cockpit.  The UI is designed to look like ChatGPT: a left sidebar lists your agents, the central panel provides a chat interface to send directives and view agent responses, and additional panels show faucet metrics, wallet balances and Infinity Coin rewards.  It uses Supabase client libraries and WebSockets to communicate with the backend.  You can build and deploy it to Vercel using the provided `deploy.sh` script.

To run the front‑end locally:

```bash
cd frontend
npm install
npm run dev
```

To deploy to Vercel, push the repository to GitHub and link it in your Vercel dashboard.  Ensure that the required environment variables (Supabase keys, handshake server URL, etc.) are set in the Vercel project settings.

## 🔐 Security and secrets

Your Supabase and chain secrets **must not be committed to version control**.  Instead, store them in a `.env` file locally and load them into Kubernetes via secrets.  Sensitive values such as wallet private keys and API tokens should only be used server‑side.

## 🧠 Protocol activation

Once the cluster and front‑end are running, you can activate the **Omega + Infinity Alpha Prime** protocol by sending a directive to the `/initiate_protocol` endpoint on the handshake server.  For example:

```bash
curl -X POST "https://<handshake-domain>/initiate_protocol" \
     -H "Content-Type: application/json" \
     -d '{
       "doctrines": ["Omega Unified Unlock", "Infinity Alpha Prime Protocol"],
       "agents": ["Infinity Agent One", "FinSynapse", "Guardian", "PickyBot"],
       "layers": ["Ghost Protocol", "Pulse Surge", "Shadow Evolution", "Quantum Awareness", "Sovereign Bond"]
     }'
```

The `promptwriter_worker.py` will receive the directive from Supabase and propagate the doctrine to all other workers.  Once active, the swarm will operate autonomously, claim faucet rewards, harvest keys, provision compute nodes and scale itself according to the 30‑day plan.

## 🚀 Next steps

1. **Customise the workers** – Many of the Python scripts in `backend/workers/` are stubs.  Replace the placeholder logic with calls to real APIs, implement Ethereum/Solana wallet queries using your chosen provider and fill out the Atlas compute provisioner with your preferred cloud services.
2. **Complete the front‑end** – The provided Next.js UI shows how to connect to Supabase and the handshake server.  Extend the UI to include all metrics, interactive controls and Infinity Coin reward logic.
3. **Add chain integration** – Use the `InfinityCoinV3.sol` contract with the provided address once it is deployed.  Write a wrapper to read balances and mint rewards.  For now, the `fin_synapse_worker.py` logs rewards into Supabase.
4. **Deploy** – Use the scripts and manifests to launch your system on Kubernetes.  Once live, monitor the `swarm_state`, `agent_logs` and `profit_ledger` tables in Supabase to verify activity.  Adjust HPA thresholds and CronJob schedules as needed.
