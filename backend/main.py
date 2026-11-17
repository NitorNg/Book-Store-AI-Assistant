from fastapi import FastAPI
from pydantic import BaseModel
from llm import ask_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post('/chat')
def sendMessage(req: ChatRequest):
        return {"Reply" : ask_llm(req.message)}

