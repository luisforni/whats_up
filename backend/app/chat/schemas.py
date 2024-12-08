from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    sender_id: int
    chat_id: int

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    user1_id: int
    user2_id: int

class ChatCreate(ChatBase):
    pass

class ChatResponse(ChatBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
