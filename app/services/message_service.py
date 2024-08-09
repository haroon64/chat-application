from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.repository.message_repository import MessageRepository
from app.schemas.message_schema import message_schema
from app.models.message import Message
from typing import Optional

class MessageService(BaseService):
    def __init__(self, message_repository:MessageRepository ):
        self.message_repository = message_repository
        super().__init__(message_repository)
    
    def save_message(self,message_info:message_schema) -> Optional[Message]:
        return self.message_repository.create_message(message_info)
    
    def get_messages(self,chat_id:str):
        print("yes")
        return self.message_repository.load_message(chat_id)
    
    
        
    
