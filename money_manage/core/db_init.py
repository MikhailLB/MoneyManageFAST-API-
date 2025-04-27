from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.transactions import TransactionsType

async def init_transactions_types(session: AsyncSession):
    result = await session.execute(select(TransactionsType))
    existing_types = result.scalars().all()

    if not existing_types:
        default_types = [
            TransactionsType(eng_name="Income", ru_name="Доход"),
            TransactionsType(eng_name="Expense", ru_name="Расход")
        ]
        session.add_all(default_types)
        await session.commit()
