from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_model import BaseModel

class Message(BaseModel, table=True):
    __tablename__ = "messages"
    
    content: str = Field()
    
    name:str = Field(foreign_key="user.name")

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="messages")