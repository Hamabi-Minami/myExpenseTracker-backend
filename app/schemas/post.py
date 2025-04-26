from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class AuthorInfo(BaseModel):
    username: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: Optional[AuthorInfo]
    likes: int = 0
    comments: list = []
    cover_url: str

    class Config:
        orm_mode = True