from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime

from app.util.schema import AllOptional


class message_schema(BaseModel):
    sender_id:int
    
    content:str
    # date_time:datetime.utcfromtimestamp
    chat_id:str



    class Config:
        orm_mode = True

class get_message(BaseModel):
    id:int
    sender_id:int
    content:str
    timestamp:datetime
