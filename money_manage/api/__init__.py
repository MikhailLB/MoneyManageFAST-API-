from fastapi import APIRouter

from .api_v1.auth.jwt_auth import router as auth_router
from .api_v1.transactions.transactions import router as transactions_router
router = APIRouter()
router.include_router(auth_router)
router.include_router(transactions_router)