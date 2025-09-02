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
