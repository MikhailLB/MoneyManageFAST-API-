from datetime import datetime, timedelta, timezone

import jwt
import bcrypt

from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth_jwt.expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire_time = now + expire_timedelta
    else:
        expire_time = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire_time,
                     iat=now,
                     )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded

def decode_jwt(token: str | bytes,
               public_key: str = settings.auth_jwt.public_key.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,
               ):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())