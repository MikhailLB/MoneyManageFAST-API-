from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from jwt import PyJWTError

from api.api_v1.auth.utils import decode_jwt


router = APIRouter()

OPEN_ENDPOINTS = [
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/open-endpoint",
    "/docs",
    "/openapi.json",
    "/redoc"]

async def jwt_middleware(request: Request, call_next):
    if request.url.path in OPEN_ENDPOINTS:
        return await call_next(request)

    token = request.cookies.get("access_token")

    if not token:
        return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

    try:
        payload = decode_jwt(token)
        request.state.user = payload

    except PyJWTError as e:
        return JSONResponse(status_code=401, content={"detail": f"Token invalid: {str(e)}"})

    return await call_next(request)