from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()
    id: Mapped[int] = mapped_column(primary_key=True)

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        col_names = list(self.__table__.columns.keys())

        for inx, col in enumerate(col_names[:max(len(col_names), self.repr_cols_num)]):
            if self.repr_cols:
                if col in self.repr_cols:
                    cols.append(f"{col}={getattr(self, col)}")
            else:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"