from contextlib import AbstractContextManager
from typing import Callable,Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.cores.config import configs
from app.cores.exceptions import DuplicatedError, NotFoundError
from app.util.query_builder import dict_to_sqlalchemy_filter_options

from app.schemas.auth_schema import SignUp
from sqlmodel import select


from typing import Callable, Optional


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model) -> None:
        self.session_factory = session_factory
        self.model = model

   
   

    
           

    def create(self, schema: SignUp) -> SignUp:
        with self.session_factory() as session:
            query = self.model(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query
            except IntegrityError as e:
                session.rollback()
                raise DuplicatedError(detail=str(e.orig))

    def update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict(exclude_none=True))
            session.commit()
            return self.read_by_id(id)

    def update_attr(self, id: int, column: str, value):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update({column: value})
            session.commit()
            return self.read_by_id(id)

    def whole_update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict())
            session.commit()
            return self.read_by_id(id)

    