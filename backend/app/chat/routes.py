from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.chat.models import Chat, Message
from app.chat.schemas import ChatCreate, ChatResponse, MessageCreate, MessageResponse

router = APIRouter()

@router.post("/chats", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    existing_chat = db.query(Chat).filter(
        ((Chat.user1_id == chat.user1_id) & (Chat.user2_id == chat.user2_id)) |
        ((Chat.user1_id == chat.user2_id) & (Chat.user2_id == chat.user1_id))
    ).first()

    if existing_chat:
        return existing_chat

    new_chat = Chat(**chat.dict())
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

@router.get("/chats/{user_id}", response_model=list[ChatResponse])
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    chats = db.query(Chat).filter((Chat.user1_id == user_id) | (Chat.user2_id == user_id)).all()
    return chats

@router.post("/messages", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/messages/{chat_id}", response_model=list[MessageResponse])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).all()
    return messages
