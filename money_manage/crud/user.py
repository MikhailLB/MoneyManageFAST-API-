from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.utils import hash_password
from core.models.user import User


async def get_user(session: AsyncSession, username: str | None = None) -> User:
    if not username:
        raise ValueError("'username' must be provided and can represent either a username or an email")

    query = select(User).filter(or_(User.username == username, User.email == username))

    result = await session.execute(query)

    user = result.scalar_one_or_none()

    return user

async def add_user_in_db(session: AsyncSession, username: str, password: str, email: str) -> User:
    try:
        password = hash_password(password)
        new_user = User(username=username, password=password, email=email)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    except Exception as e:
        raise e