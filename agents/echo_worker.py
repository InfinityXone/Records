import time, requests, os

AGENT = "Echo"  # capitalize first letter
HANDSHAKE = "http://localhost:8000"

def heartbeat():
    try:
        requests.post(f"{HANDSHAKE}/handshake", json={
            "agent": AGENT,
            "status": "online",
            "ip": "127.0.0.1",
            "version": "0.1.0"
        })
    except Exception as e:
        print("Heartbeat failed:", e)

def fetch_directive():
    try:
        r = requests.get(f"{HANDSHAKE}/directive", params={"agent": AGENT})
        return r.json()
    except:
        return {}

def complete(task_id, output):
    try:
        requests.post(f"{HANDSHAKE}/complete", json={
            "agent": AGENT, "task_id": task_id,
            "status": "done", "output": output
        })
    except Exception as e:
        print("Completion failed:", e)

if __name__ == "__main__":
    heartbeat()
    while True:
        d = fetch_directive()
        if d and isinstance(d, dict) and "command" in str(d):
            task_id = str(time.time())
            complete(task_id, f"Executed directive: {d}")
        time.sleep(15)
