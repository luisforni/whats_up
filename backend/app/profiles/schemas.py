from pydantic import BaseModel

class ProfileCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    birth_date: str
    bio: str

class ProfileResponse(ProfileCreate):
    id: int

    class Config:
        orm_mode = True
