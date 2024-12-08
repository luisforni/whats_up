from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    content: str

class PostCreate(BaseModel):
    user_id: int
    content: str

class PostResponse(PostCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True