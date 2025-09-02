#!/bin/bash
set -e

echo "🌌 [Infinity X One] Omega + Rosetta + FinSynapse Expansion Bootstrap"
BASE_DIR="/opt/infinity_x_one"
cd $BASE_DIR
mkdir -p logs

# --- Python venv ---
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Requirements
cat > requirements.txt <<'REQ'
supabase
fastapi
uvicorn
requests
paramiko
python-dotenv
beautifulsoup4
feedparser
redis
REQ
pip install -r requirements.txt

# --- IntellaBot (Internet/GitHub Scout) ---
cat > intellabot.py <<'PY'
#!/usr/bin/env python3
import requests, time, supabase, feedparser
from bs4 import BeautifulSoup
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def scrape_github():
    r = requests.get("https://github.com/trending/python?since=daily")
    soup = BeautifulSoup(r.text, "html.parser")
    repos = [a.text.strip() for a in soup.find_all("h2", class_="lh-condensed")]
    return repos

def scrape_arxiv():
    feed = feedparser.parse("http://export.arxiv.org/rss/cs.AI")
    return [e.title for e in feed.entries]

def loop():
    while True:
        gh = scrape_github()
        ax = scrape_arxiv()
        client.table("agent_logs").insert({
            "agent":"IntellaBot",
            "task":"scout",
            "log": f"GH: {gh[:5]}, Arxiv: {ax[:5]}",
            "ts": time.time()
        }).execute()
        time.sleep(3600)  # every hour

if __name__ == "__main__":
    loop()
PY
chmod +x intellabot.py

# --- FinSynapse Scraper (Financial Anomalies) ---
cat > finsynapse_scraper.py <<'PY'
#!/usr/bin/env python3
import requests, time, supabase, os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

TARGETS = [
    "https://faucetpay.io/list",
    "https://airdrops.io/",
    "https://defillama.com/yields"
]

def loop():
    while True:
        for url in TARGETS:
            try:
                r = requests.get(url, timeout=20)
                snippet = r.text[:200]
                client.table("agent_logs").insert({
                    "agent":"FinSynapse",
                    "task":"scan",
                    "log": f"{url} -> {snippet}",
                    "ts": time.time()
                }).execute()
            except Exception as e:
                client.table("agent_logs").insert({
                    "agent":"FinSynapse",
                    "task":"error",
                    "log": str(e),
                    "ts": time.time()
                }).execute()
        time.sleep(1800) # every 30 min

if __name__ == "__main__":
    loop()
PY
chmod +x finsynapse_scraper.py

# --- systemd services ---
cat > /etc/systemd/system/intellabot.service <<'SERVICE'
[Unit]
Description=IntellaBot - Internet/GitHub Scout
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/python /opt/infinity_x_one/intellabot.py
WorkingDirectory=/opt/infinity_x_one
Restart=always
StandardOutput=append:/opt/infinity_x_one/logs/intellabot.log
StandardError=append:/opt/infinity_x_one/logs/intellabot.err

[Install]
WantedBy=multi-user.target
SERVICE

cat > /etc/systemd/system/finsynapse_scraper.service <<'SERVICE'
[Unit]
Description=FinSynapse Scraper - Faucets & Financial Anomalies
After=network.target

[Service]
ExecStart=/opt/infinity_x_one/venv/bin/python /opt/infinity_x_one/finsynapse_scraper.py
WorkingDirectory=/opt/infinity_x_one
Restart=always
StandardOutput=append:/opt/infinity_x_one/logs/finsynapse_scraper.log
StandardError=append:/opt/infinity_x_one/logs/finsynapse_scraper.err

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reexec
systemctl enable intellabot finsynapse_scraper
systemctl restart intellabot finsynapse_scraper

echo "===================================================="
echo "✅ Omega Expansion: IntellaBot + FinSynapse Hunter live."
echo "✅ Agents will now 24/7 scout GitHub, arXiv, faucets, anomalies."
echo "✅ Logs writing to Supabase -> agent_logs."
