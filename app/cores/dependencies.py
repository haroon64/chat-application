from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app.cores.config import configs
from app.cores.container import Container
from app.cores.exceptions import AuthError
from app.cores.security import ALGORITHM, JWTBearer
from app.models.user import User
# from app.schemas.auth_schema import Payload
from app.services.user_service import UserService


@inject
def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Extract email from the 'sub' field
        if email is None:
            raise AuthError(detail="Token missing user email")
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    
    current_user: User = service.get_by_email(email)
    if not current_user:
        raise AuthError(detail=f"User not found with email: {email}")
    return current_user


# def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
#     if not current_user.is_active:
#         raise AuthError("Inactive user")
#     return current_user


# def get_current_user_with_no_exception(
#     token: str = Depends(JWTBearer()),
#     service: UserService = Depends(Provide[Container.user_service]),
# ) -> User:
#     try:
#         payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
#         token_data = Payload(**payload)
#     except (jwt.JWTError, ValidationError):
#         return None
#     current_user: User = service.get_by_id(token_data.id)
#     if not current_user:
#         return None
#     return current_user


# def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
#     if not current_user.is_active:
#         raise AuthError("Inactive user")
#     if not current_user.is_superuser:
#         raise AuthError("It's not a super user")
#     return current_user
