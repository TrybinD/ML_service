from hashlib import md5

from fastapi import HTTPException

from service.api.schemas import UserLogin, UserRegister, SignInResponse, User
from service.api.repositories.base import AbstractRepository
from service.api.security import create_access_token
from service.api.models import DBUser
from service.api.repositories.user_repo import UserRepository



class UserService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def get_balance(self, user: User) -> int:

        db_user: DBUser = await self.users_repo.find_by_options(id=user.id, unique=True)

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return db_user.balance
    
def user_service():
    return UserService(UserRepository)
