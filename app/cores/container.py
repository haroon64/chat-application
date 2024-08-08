from dependency_injector import containers, providers
from app.cores.config import configs
from app.cores.database import Database
from app.repository.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.message_service import MessageService
from app.repository.message_repository import MessageRepository

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.message",
            
            "app.cores.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    message_reposiory=providers.Factory(MessageRepository, session_factory=db.provided.session)
   

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    message_service=providers.Factory(MessageService, message_reposiory=message_reposiory)
    