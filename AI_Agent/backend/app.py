from fastapi import FastAPI
from pydantic import BaseModel
from conversation import chat_with_memory
from voice import record_and_transcribe

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    response = chat_with_memory(req.message)
    return {"response": response}

@app.post("/transcribe")
async def transcribe_endpoint():
    try:
        text = record_and_transcribe(duration=5)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}