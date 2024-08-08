from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.repository.message_repository import MessageRepository
from app.schemas.message_schema import message_schema

class MessageService(BaseService):
    def __init__(self, message_repository:MessageRepository ):
        self.message_repository = message_repository
        super().__init__(message_repository)
    
    def save_message(self,message_info:message_schema):
        return self.message_repository.create_message(message_info)

    
        
    
