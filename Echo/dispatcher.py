import json
import subprocess
import time
from pathlib import Path

pipe = Path("/opt/infinity_x_one/Echo/commands.json")

def log(msg):
    with open("/opt/infinity_x_one/Echo/logs/agent.log", "a") as f:
        f.write(f"{time.ctime()} | {msg}\n")

while True:
    if pipe.exists():
        try:
            with open(pipe) as f:
                cmd = json.load(f)
            log(f"🔗 Received: {cmd.get('command')}")

            if cmd.get("command") == "pull_and_execute":
                subprocess.run([
                    "git", "clone", cmd["payload"]["repo_url"], cmd["payload"]["target_path"]
                ])
                for line in cmd["payload"]["post_pull"]:
                    subprocess.run(line, shell=True)
                log("✅ Command executed successfully.")
            else:
                log("⚠️ Unknown command.")

        except Exception as e:
            log(f"❌ Error: {str(e)}")
        pipe.unlink()
    time.sleep(5)
