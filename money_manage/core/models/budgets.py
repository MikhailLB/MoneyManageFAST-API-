from sqlalchemy import String, nullsfirst
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from core.db_connection.database import Base

class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    transactions: Mapped[list['Transactions']] = relationship(back_populates='category')