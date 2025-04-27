from sqlalchemy.ext.asyncio import AsyncSession

from core.models.transactions import Transactions
from core.schemas.transaction import TransactionIn


async def add_transaction_in_db(session: AsyncSession, transaction: TransactionIn) -> Transactions:
    try:
        transaction = Transactions(**transaction.model_dump())

        session.add(transaction)

        await session.commit()
        await session.refresh(transaction)

        return transaction

    except Exception as e:
        raise e
