from sqlmodel import Field
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


from app.models.base_model import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "user"
   
    
    email: str = Field(unique=True)
    password: str = Field()
    user_token: str = Field(unique=True)
    name: str = Field(default=None, nullable=True, unique=True)
    
    messages: List["Message"] = Relationship(back_populates="user")
