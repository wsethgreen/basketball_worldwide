from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.division import Division


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str]
    nickname: Mapped[str]
    budget: Mapped[int | None] = mapped_column()
    division_id: Mapped[int] = mapped_column(
        ForeignKey("divisions.id"), index=True, nullable=False
    )

    division: Mapped["Division"] = relationship("Division", back_populates="teams")
