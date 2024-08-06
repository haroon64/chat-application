from datetime import timedelta
from typing import List, Optional

from app.cores.config import configs
from app.cores.exceptions import AuthError
from app.cores.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.auth_schema import SignIn, SignUp
from app.schemas.auth_schema import SignInResponse
from app.services.base_service import BaseService
from app.util.hash import get_rand_hash


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn) -> Optional[SignInResponse]:
        user = self.user_repository.get_by_email(sign_in_info.email)
        
   
        if user and verify_password(sign_in_info.password, user.password):
            token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token, expiration_datetime = create_access_token({"sub": user.email}, token_lifespan)
            sign_in_result = SignInResponse(
                access_token=access_token,
                expiration=expiration_datetime,
                user_info=user
            )
            return sign_in_result

    def sign_up(self, user_info: SignUp):
        user_token = get_rand_hash()
        user = User(**user_info.dict(exclude_none=True),  user_token=user_token)
        user.password = get_password_hash(user_info.password)
        print("pasword is ::::: ",user.password)
        print("::",user.user_token)
        created_user = self.user_repository.create(user)
       
        return created_user
