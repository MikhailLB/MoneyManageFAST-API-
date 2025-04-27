from datetime import timedelta

from pycparser.ply.yacc import token

from api.api_v1.auth.utils import encode_jwt
from core.config import settings
from core.models.user import User
from core.schemas.user import UserOut

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(token_type: str, token_data: dict,
               expire_minutes: int = settings.auth_jwt.expire_minutes,
               expire_timedelta: timedelta | None = None,) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type,}
    jwt_payload.update(token_data)
    return encode_jwt(jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta)

def create_access_token(user) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    return create_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload, expire_minutes=settings.auth_jwt.expire_minutes,)

def create_refresh_token(user) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    return create_jwt(token_type=REFRESH_TOKEN_TYPE,token_data=jwt_payload, expire_minutes=settings.auth_jwt.refresh_token_expire_minutes,)