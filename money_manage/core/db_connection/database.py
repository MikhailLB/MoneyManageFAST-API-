from sqlalchemy import MetaData
from sqlalchemy import DeclarativeBase
from sqlalchemy import Mapped
from sqlalchemy.testing.schema import mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()
    id: Mapped[int] = mapped_column(primary_key=True)

