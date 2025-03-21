# models.py
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(...)
    message: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
