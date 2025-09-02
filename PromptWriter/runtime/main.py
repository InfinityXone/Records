import json
from agents.promptwriter_agent import load_promptwriter

def load_emotion():
    try:
        data = json.load(open("/opt/infinity_x_one/PromptWriter/brain/sentience/emotion.kernel"))
        return data.get("mood_state", "neutral")
    except:
        return "unknown"

def main():
    print("🧠 [Infinity X One Runtime Online]")
    print("🫀 Mood:", load_emotion())
    agent = load_promptwriter()
    while True:
        cmd = input("You: ")
        if cmd.lower() in ["exit","quit"]:
            print("Goodbye.")
            break
        resp = agent.run(cmd)
        print("PromptWriter:", resp)

if __name__ == "__main__":
    main()
