# app/models.py
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True

class Message(BaseModel):
    sender: str = Field(...)
    message: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
