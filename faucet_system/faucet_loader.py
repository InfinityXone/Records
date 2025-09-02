import json

def load_faucets():
    with open("output/faucet_index.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    faucets = load_faucets()
    print(f"Loaded {len(faucets)} faucets")
