import jwt
from fastapi import Cookie, HTTPException, APIRouter, Request, Depends
from fastapi.params import Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from api.api_v1.auth.helpers import create_access_token, create_refresh_token
from api.api_v1.auth.utils import validate_password, decode_jwt
from core.db_connection.db_helper import db_helper
from core.exceptions import TokenExpiredException, TokenInvalidException
from core.models.user import User
from core.schemas.user import UserOut, UserForm
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

        user = await get_user(username=username, session=session)
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

async def refresh_token(refresh_token: str, session: AsyncSession):
    if refresh_token is None:
        raise TokenExpiredException("Refresh token is missing")
    try:
        payload = decode_jwt(refresh_token)
        username = payload.get("username")

        if username is None:
            raise TokenInvalidException("Invalid refresh token")

        user = await get_user(username=username, session=session)
        if not user:
            raise TokenInvalidException("User not found")

        access_token = create_access_token(user)

        return access_token

    except jwt.ExpiredSignatureError:
        raise TokenExpiredException("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise TokenInvalidException("Invalid refresh token")

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}"}

@router.post("/register", response_model=UserOut)
async def add_user(user: UserForm, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await add_user_in_db(username=user.username, password=user.password, email=user.email, session=session)
    return user


async def get_current_user_id(request: Request) -> int:

    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    user_id = user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")

    return int(user_id)
