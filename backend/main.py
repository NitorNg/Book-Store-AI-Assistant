from fastapi import FastAPI
from pydantic import BaseModel
from llm import ask_llm
from fastapi.middleware.cors import CORSMiddleware
from authentication import router as auth_router 

app = FastAPI()
app.include_router(auth_router) 

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
    return {"Reply": ask_llm(req.message)}
