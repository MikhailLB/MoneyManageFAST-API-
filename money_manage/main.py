from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from api import router as api_router
from middleware.auth import jwt_middleware
from fastapi.middleware.cors import CORSMiddleware
from money_manage.core.config import settings
from core.db_connection.db_helper import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shutdown
    db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)


main_app.middleware("http")(jwt_middleware)
main_app.include_router(api_router,
                        prefix=settings.api.prefix,)

if __name__ == '__main__':
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )