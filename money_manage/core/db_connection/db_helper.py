from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from money_manage.core.config import settings

class DatabaseHelper:
    def __init__(self,
                 url: str,
                 echo: bool = False,
                 echo_pool: bool = False,
                 max_overflow: int = 10,
                 pool_size: int = 10,
                 ):
        self.engine = create_async_engine(url=url,
                                          echo=echo,
                                          echo_pool=echo_pool,
                                          max_overflow=max_overflow,
                                          pool_size=pool_size
                                          )

        self.session_factory = async_sessionmaker(bind=self.engine,
                                                  autocommit=False,
                                                  autoflush=False,
                                                  expire_on_commit=False)
    async def dispose(self):
        await self.engine.dispose()

    @asynccontextmanager
    async def session_getter_md(self):
        async with self.session_factory() as session:
            yield session

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session

db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)