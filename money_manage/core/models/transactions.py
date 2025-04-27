from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, foreign, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Date, CheckConstraint, DECIMAL
from datetime import date
from core.db_connection.database import Base
from core.models.budgets import Category
from core.models.user import User
from core.models.currencies import Currency

class Transactions(Base):
    __tablename__ = 'transactions'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    amount: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    transaction_type_id: Mapped[int] = mapped_column(ForeignKey('transactions_type.id'))
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )

    category: Mapped["Category"] = relationship(back_populates="transactions")
    user: Mapped["User"] = relationship(back_populates="transactions")
    transaction_type: Mapped["TransactionsType"] = relationship(back_populates="transactions")
    currency: Mapped["Currency"] = relationship(back_populates="transactions")

    __table_args__ = (
        CheckConstraint('amount >= 0 AND amount <= 999999999999', name='check_amount_positive'),
    )


class TransactionsType(Base):
    __tablename__ = 'transactions_type'

    eng_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    ru_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    transactions: Mapped[list["Transactions"]] = relationship(back_populates="transaction_type")
