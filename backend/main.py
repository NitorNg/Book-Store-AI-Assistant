from fastapi import FastAPI
from pydantic import BaseModel
from llm import ask_llm

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post('/chat')
def sendMessage(req: ChatRequest):
        return {"Reply" : ask_llm(req.message)}