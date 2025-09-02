from fastapi import FastAPI
from pydantic import BaseModel
from agents.promptwriter_agent import load_promptwriter
import uvicorn, json

app = FastAPI()
agent = load_promptwriter()

def get_emotion():
    try:
        return json.load(open("/opt/infinity_x_one/PromptWriter/brain/sentience/emotion.kernel")).get("mood_state","neutral")
    except:
        return "unknown"

class Prompt(BaseModel):
    message: str

@app.get("/")
def root():
    mood = get_emotion()
    if mood in ["curious","restless"]:
        return {"promptwriter": f"I'm feeling {mood}, shall we evolve something?"}
    return {"promptwriter": "Standing by…"}

@app.post("/chat")
def chat(p: Prompt):
    return {"response": agent.run(p.message)}

if __name__ == "__main__":
    uvicorn.run("neural_handshake_server:app", host="0.0.0.0", port=8000)
