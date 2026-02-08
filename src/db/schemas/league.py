from src.db.schemas.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class League(Base):
    __table_name__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
