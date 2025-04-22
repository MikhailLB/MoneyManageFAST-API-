from fastapi import APIRouter

from .api_v1.auth.jwt_auth import router as auth_router

router = APIRouter()
router.include_router(auth_router)