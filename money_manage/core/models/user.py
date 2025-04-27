from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime

from core.db_connection.database import Base


class User(Base):
    __tablename__ = 'users'

    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    transactions: Mapped[list['Transactions']] = relationship(back_populates="user",cascade="all, delete-orphan")