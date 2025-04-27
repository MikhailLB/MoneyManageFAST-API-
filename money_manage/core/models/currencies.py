from datetime import datetime, timezone

from sqlalchemy import String, DECIMAL, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from core.db_connection.database import Base



class Currency(Base):
    __tablename__ = 'currencies'

    code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    exchange_rate: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )

    transactions: Mapped[list["Transactions"]] = relationship(back_populates="currency")