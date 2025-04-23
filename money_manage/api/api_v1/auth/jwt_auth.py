from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, APIRouter
from fastapi.params import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import session_user
from starlette.responses import JSONResponse

from api.api_v1.auth.helpers import create_access_token, create_refresh_token
from api.api_v1.auth.utils import validate_password, decode_jwt
from core.db_connection.db_helper import db_helper
from core.models.user import User
from core.schemas.user import UserOut, UserIn, UserForm
from crud.user import get_user, add_user_in_db

router = APIRouter(prefix="/auth",
    tags=["auth"],)

async def authenticate_user(password: str, session: AsyncSession, username: str | None = None):
    user = await get_user(username=username, session=session)
    if user and validate_password(password, user.password):
        return user
    else:
        return None


async def get_current_user(
        token: str = Cookie(default=None, alias="access_token"),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    if token is None:
        raise HTTPException(status_code=401, detail="No access token provided")

    try:
        payload = decode_jwt(token)
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await get_user(username=username, session=session)  # нужно ждать!
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/login")
async def login(username: str = Form(), password: str = Form(), session: AsyncSession = Depends(db_helper.session_getter)):
    """
            Login user
    """
    user = await authenticate_user(username=username, password=password, session=session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/email or password")
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response = JSONResponse(content={"message": "Logged in"})
    response.set_cookie("access_token", access_token, httponly=True, secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
    return response

@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Cookie(default=None, alias="refresh_token"),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    """
            Get refresh token
    """
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    try:
        payload = decode_jwt(refresh_token)
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await get_user(username=username, session=session)  # await обязательно
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(user)
        response = JSONResponse(content={"message": "Token refreshed"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True
        )
        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}"}

@router.post("/register", response_model=UserOut)
async def add_user(user: UserForm, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await add_user_in_db(username=user.username, password=user.password, email=user.email, session=session)
    return user

@router.get("/check")
async def check():
    return {"message": f"Hello, it not working"}