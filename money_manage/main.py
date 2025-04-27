from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from api import router as api_router
from core.db_init import init_transactions_types
from middleware.auth import jwt_middleware
from money_manage.core.config import settings
from core.db_connection.db_helper import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.session_getter_md() as session:
        await init_transactions_types(session)
    yield
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