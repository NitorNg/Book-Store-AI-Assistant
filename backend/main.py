from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

message = "hello"

class ChatRequest(BaseModel):
    message: str

@app.get('/')
def root():
    if "hello" in message:
        return "Welcome to the chat bot"
    

@app.post('/chat')
def sendMessage(req: ChatRequest):
    if "hello" in req.message.lower():
        return {"Reply" : "Welcome to chatbot"}
    return{"Reply": "Im not sure yet"}