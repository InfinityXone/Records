#!/usr/bin/env python3
import os, time, requests
from bs4 import BeautifulSoup
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log(msg): print(f"[ScraperX] {msg}")

def save_discovery(kind, name, url):
    supabase.table("discoveries").insert({
        "kind": kind, "name": name, "url": url
    }).execute()
    log(f"Saved discovery: {name} ({kind})")

def scrape_github_trending():
    url = "https://github.com/trending/python?since=daily"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    for repo in soup.find_all("h2", class_="h3"):
        name = repo.text.strip().replace("\n", "").replace(" ", "")
        href = "https://github.com" + repo.a["href"]
        save_discovery("github", name, href)

def scrape_faucet_list():
    url = "https://cryptofaucets.org/"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "faucet" in href:
            save_discovery("faucet", link.text.strip() or href, href)

if __name__ == "__main__":
    log("Starting ScraperX Worker…")
    while True:
        try:
            scrape_github_trending()
            scrape_faucet_list()
        except Exception as e:
            log(f"Error: {e}")
        time.sleep(3600)  # run once per hour
