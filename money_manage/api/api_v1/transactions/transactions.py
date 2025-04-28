from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.auth.jwt_auth import get_current_user_id
from core.db_connection.db_helper import db_helper
from core.schemas.transaction import TransactionIn, TransactionOut
from crud.transactions import add_transaction_in_db, get_transaction_by_id

router = APIRouter(prefix="/transactions",
    tags=["transaction"],)

@router.post("/add", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def add_transaction(
    transaction_in: TransactionIn,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),

):
    """
    Create a new transaction.

    This endpoint allows an authenticated user to create a new transaction. The user ID is automatically
    attached from the JWT token, and the transaction data is validated before insertion into the database.

    **Request Body:**
    - `user_id` (int): The ID of the user (extracted from the JWT token)
    - `category_id` (int): The ID of the category associated with the transaction.
    - `description` (str): A brief description of the transaction.
    - `amount` (float): The amount of money for the transaction.
    - `transaction_type_id` (int): The type of transaction (e.g., income or expense).
    - `currency_id` (int): The ID of the currency used in the transaction.
    - `created_at` (datetime): The time when the transaction was created (optional).
    - `updated_at` (datetime): The time when the transaction was last updated (optional).

    **Responses:**
    - **201 Created**: Successfully created a transaction.
      - Returns the created transaction object.
    - **400 Bad Request**: Invalid input data, failed to create a transaction.
      - `detail`: Error message explaining what went wrong.
    - **500 Internal Server Error**: Database error during the transaction creation process.
    """

    try:
        transaction_in.user_id = int(user_id)
        transaction = await add_transaction_in_db(transaction=transaction_in, session=session)
    except SQLAlchemyError as db_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating transaction: {db_error}"
        )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create transaction. Invalid input data."
        )

    return transaction


@router.get("/get_transaction", response_model=TransactionOut, status_code=status.HTTP_200_OK)
async def get_transaction(transaction_id: int,
                          user_id: str = Depends(get_current_user_id),
                          session: AsyncSession = Depends(db_helper.session_getter)
                          ):
    """
        Get a transaction.

        This endpoint allows an authenticated user to get a new transaction. The user ID is automatically
        attached from the JWT token.

        **Request Body:**
        - `user_id` (int): The ID of the user (extracted from the JWT token)
        - `transaction_id`: The ID of the transaction.

        **Responses:**
        - **200 Fetched**: Successfully fetched a transaction.
          - Returns the fetched transaction object.
        - **400 Bad Request**: Invalid input data, failed to fetch a transaction.
          - `detail`: Error message explaining what went wrong.
        - **500 Internal Server Error**: Database error during the transaction creation process.
        """

    try:
        transaction = await get_transaction_by_id(transaction_id=transaction_id, user_id=user_id, session=session)

        if transaction:
            return transaction
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    except SQLAlchemyError as db_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error while getting transaction: {db_error}")

