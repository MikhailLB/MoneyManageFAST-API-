from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from jwt import PyJWTError

from api.api_v1.auth.jwt_auth import refresh_token
from api.api_v1.auth.utils import decode_jwt
from core.exceptions import TokenExpiredException, TokenInvalidException

router = APIRouter()

OPEN_ENDPOINTS = [
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/open-endpoint",
    "/docs",
    "/openapi.json",
    "/redoc"]


async def jwt_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")
    refr_token = request.cookies.get("refresh_token")

    if request.url.path not in OPEN_ENDPOINTS:
        if not token:
            if refr_token:
                try:
                    access_token = await refresh_token(session=request.state.session)
                    response = await call_next(request)
                    response.set_cookie("access_token", access_token, httponly=True, secure=True)
                    return response

                except (TokenExpiredException, TokenInvalidException) as e:
                    return JSONResponse(status_code=401, content={"detail": str(e)})
            else:
                return JSONResponse(status_code=401, content={"detail": "Missing authorization token"})

        try:
            payload = decode_jwt(token)
            request.state.user = payload

        except (TokenExpiredException, TokenInvalidException) as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})
        return await call_next(request)
    return await call_next(request)