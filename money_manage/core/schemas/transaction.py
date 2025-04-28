from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class TransactionBase(BaseModel):
    user_id: int | None = None
    category_id: int
    description: str | None = None
    amount: float
    transaction_type_id: int
    currency_id: int


class TransactionIn(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    date: date
    created_at: datetime
    updated_at: datetime

class TransactionListResponse(BaseModel):
    total: int
    items: List[TransactionOut]


class TransactionUpdate(BaseModel):
    user_id: int | None = None
    category_id: int | None = None
    description: str | None = None
    amount: float | None = None
    transaction_type_id: int | None = None
    currency_id: int | None = None
