from typing import Annotated
import asyncio

from fastapi import APIRouter, Depends

from service.api.schemas import UserLogin, UserRegister, SignInResponse, User
from service.api.services.auth_service import AuthService, auth_service
from service.api.services.user_service import UserService, user_service
from service.api.security import get_current_user_from_cookie


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in")
async def sign_in(user_login_info: UserLogin, auth_service: Annotated[AuthService, Depends(auth_service)]) -> SignInResponse:
    """Sign in user. Returns token for user and saves it to cookie"""
    response = await auth_service.sing_in(user_login_info)
    return response


@router.post("/sign-up")
async def sign_up(user_register_info: UserRegister, auth_service: Annotated[AuthService, Depends(auth_service)]) -> SignInResponse:
    """Sign up user. Returns token for user and saves it to cookie"""
    response = await auth_service.sign_up(user_register_info)
    return response


@router.get("/get-balance")
async def get_balance(user_service: Annotated[UserService, Depends(user_service)], 
                      current_user: User = Depends(get_current_user_from_cookie)) -> int:
    """Get user balance"""

    balance = await user_service.get_balance(current_user)
    await asyncio.sleep(5)

    return balance
