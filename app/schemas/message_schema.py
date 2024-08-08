from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime

from app.util.schema import AllOptional


class message_schema(BaseModel):
    client_id:str
    
    content:str
    date_time:datetime
    chat_id:str



    class Config:
        orm_mode = True