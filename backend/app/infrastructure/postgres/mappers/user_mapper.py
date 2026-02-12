from app.infrastructure.postgres.models.user import User
from app.domain.entities.user_entity import UserEntity

class UserMapper:
    @staticmethod
    def to_domain(db_user: User) -> UserEntity:
        return UserEntity(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at
        )
