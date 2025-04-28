from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import exclude

from core.models.transactions import Transactions
from core.models.user import User
from core.schemas.transaction import TransactionIn, TransactionUpdate


async def add_transaction_in_db(session: AsyncSession, transaction: TransactionIn) -> Transactions:
    try:
        transaction = Transactions(**transaction.model_dump())

        session.add(transaction)

        await session.commit()
        await session.refresh(transaction)

        return transaction

    except Exception as e:
        raise e

async def get_transaction_by_id(session: AsyncSession, transaction_id: int, user_id: str) -> Transactions:
    try:
        query = select(Transactions).filter(and_(Transactions.id == transaction_id, Transactions.user_id == user_id))
        transaction = await session.execute(query)
        result = transaction.scalar_one_or_none()
        return result

    except Exception as e:
        raise e

async def get_transactions_db(session: AsyncSession, limit: int, offset: int, user_id: str) -> Sequence[Transactions]:
    try:
        query = select(Transactions).filter(Transactions.user_id == user_id).offset(offset).limit(limit)
        transactions = await session.execute(query)
        result = transactions.scalars().all()
        return result

    except Exception as e:
        raise e

async def update_transaction_db(session: AsyncSession, transaction_update: TransactionUpdate, transaction_id: int) -> Transactions:
    try:
        result = await session.execute(
            select(Transactions).filter(
                and_(
                    Transactions.id == transaction_id,
                    Transactions.user_id == transaction_update.user_id
                )
            )
        )
        db_transaction = result.scalar_one_or_none()

        if db_transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")

        update_data = transaction_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_transaction, key, value)

        await session.commit()
        await session.refresh(db_transaction)

        return db_transaction

    except Exception as e:
        raise e