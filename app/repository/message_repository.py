from contextlib import AbstractContextManager
from typing import Callable, Optional
from app.cores.exceptions import DuplicatedError, NotFoundError


from sqlalchemy.orm import Session

from app.models.message import Message
from app.repository.base_repository import BaseRepository
from sqlmodel import select,Session
from app.schemas.message_schema import message_schema
from sqlalchemy.exc import IntegrityError



class MessageRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Message)
    
    def create_message(self,message_info:message_schema):
          with self.session_factory() as session:
            query = self.model(**message_info.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query
            except IntegrityError as e:
                session.rollback()
                raise DuplicatedError(detail=str(e.orig))

