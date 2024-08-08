from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_model import BaseModel
from datetime import datetime


class Message(BaseModel, table=True):
    __tablename__ = "messages"
    



    content: str = Field()
    sender_id: int = Field(foreign_key="user.id")

    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    chat_id:str=Field(default='1234')

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="messages")

    