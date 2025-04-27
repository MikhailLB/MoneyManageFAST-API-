from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.auth.jwt_auth import get_current_user_id
from core.db_connection.db_helper import db_helper
from core.schemas.transaction import TransactionIn, TransactionOut
from crud.transactions import add_transaction_in_db

router = APIRouter(prefix="/transactions",
    tags=["transaction"],)

@router.post("/add", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def add_transaction(
    transaction_in: TransactionIn,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),

):

    try:
        transaction_in.user_id = int(user_id)
        transaction = await add_transaction_in_db(transaction=transaction_in, session=session)
    except SQLAlchemyError as db_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating transaction"
        )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create transaction. Invalid input data."
        )

    return transaction
