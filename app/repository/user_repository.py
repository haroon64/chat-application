from contextlib import AbstractContextManager
from typing import Callable, Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.repository.base_repository import BaseRepository
from sqlmodel import select,Session


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        with self.session_factory() as session:
            return session.query(User).filter(User.email == email).first()
