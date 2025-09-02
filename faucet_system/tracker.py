#######################################
# Self-Heal Missing Scripts
#######################################
if [ ! -f $BASE/faucet_system/tracker.py ]; then
  cat <<'EOF' > $BASE/faucet_system/tracker.py
import json
def track_event(event):
    with open("swarm_tracker.log", "a") as f:
        f.write(json.dumps(event) + "\n")
if __name__ == "__main__":
    track_event({"status": "tracker online"})
EOF
fi

if [ ! -f $BASE/faucet_system/faucet_loader.py ]; then
  cat <<'EOF' > $BASE/faucet_system/faucet_loader.py
import json
def load_faucets():
    with open("output/faucet_index.json", "r") as f:
        return json.load(f)
if __name__ == "__main__":
    faucets = load_faucets()
    print(f"Loaded {len(faucets)} faucets")
EOF
fi
