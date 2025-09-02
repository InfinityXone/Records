-- 🧬 Infinity X One | Faucet & Wallet Tracking Schema
-- Create table for faucet profits
create table if not exists profit_ledger (
  id uuid primary key default gen_random_uuid(),
  ts timestamptz default now(),
  wallet text not null,
  asset text not null,
  delta numeric not null,
  note text,
  tx_hash text
);

-- Create table for agent logs (wallet balances, actions, events)
create table if not exists agent_logs (
  id uuid primary key default gen_random_uuid(),
  ts timestamptz default now(),
  agent_id text not null,
  action text not null,
  details jsonb
);

-- Create table for swarm state (agent/shard registration)
create table if not exists swarm_state (
  id uuid primary key default gen_random_uuid(),
  agent_id text not null,
  shard text,
  ts timestamptz default now()
);

-- Create table for integrity events (Guardian + PickyBot reviews)
create table if not exists integrity_events (
  id uuid primary key default gen_random_uuid(),
  ts timestamptz default now(),
  actor text not null,
  subject text not null,
  decision text not null,
  reason text
);
