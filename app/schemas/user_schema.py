from typing import List, Optional

from pydantic import BaseModel


from app.util.schema import AllOptional


class User(BaseModel):
    id:int
   
    email:str
   
    password:str
    user_token:str
    name:str




    class Config:
        orm_mode = True