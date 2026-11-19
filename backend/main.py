from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from llm import ask_llm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Conversation, Messages
from database import get_db, Base, engine
from authentication import router as auth_router 

Base.metadata.create_all(bind=engine)


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
    conversation_id: int | None = None

@app.post('/chat')
def sendMessage(req: ChatRequest, db: Session = Depends(get_db)):
    if req.conversation_id is None:
        conv = Conversation()
        db.add(conv)
        db.commit()
        db.refresh(conv)
    else:
        conv = (
        db.query(Conversation)
        .filter(Conversation.id == req.conversation_id)
        .first()
        )
        if conv == None:
                raise HTTPException(status_code=404, detail= "Conversation Not Found")
    
    messages_rows = db.query(Messages).filter(Messages.conversation_id == conv.id).order_by(Messages.created_at).all()

    history = [{"role": m.role, "content": m.text, "created_at": m.created_at} for m in messages_rows[-10:]]
    history.append({"role": "user", "content": req.message  })

    print(history)
    reply = ask_llm(req.message, history)

    db.add(Messages(conversation_id= conv.id, role="user", text = req.message))
    db.add(Messages(conversation_id = conv.id, role = "bot", text = reply))
    db.commit()

    return {"conversation_id": conv.id, "reply": reply}
    



