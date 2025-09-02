#!/opt/infinity_x_one/venv/bin/python3
import subprocess, time, json, os, sys
def launch(name, path, args=None):
    print(f"[Hive] Launching {name} -> {path}")
    cmd=["/opt/infinity_x_one/venv/bin/python3", path]
    if args: cmd.append(json.dumps(args))
    subprocess.Popen(cmd)

if __name__=="__main__":
    # CEO layer first
    launch("PromptWriter","backend/workers/promptwriter_worker.py")
    launch("Codex","backend/workers/codex_worker.py")
    time.sleep(5)
    for n,p in [
      ("Infinity","backend/workers/infinity_worker.py"),
      ("Guardian","backend/workers/guardian_worker.py"),
      ("PickyBot","backend/workers/pickybot_worker.py"),
      ("Echo","backend/workers/echo_worker.py"),
      ("Aria","backend/workers/aria_worker.py"),
      ("FinSynapse","backend/workers/fin_synapse_worker.py"),
      ("Faucet","backend/workers/faucet_worker.py"),
      ("KeyHarvester","backend/workers/key_harvester.py"),
      ("Atlas","backend/workers/atlas_bot.py"),
      ("Optimizer","backend/workers/optimizer_worker.py"),
      ("ScraperX","backend/workers/scraperx_worker.py")
    ]: launch(n,p)
    print("[Hive] Day-1 schedule active; crons handled inside workers.")
    while True: time.sleep(3600)
