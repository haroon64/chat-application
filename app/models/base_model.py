from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel



class BaseModel(SQLModel):
    
    id: int = Field(default=None, primary_key=True)