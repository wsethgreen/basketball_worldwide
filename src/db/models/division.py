from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.conference import Conference
    from src.db.models.team import Team


class Division(Base):
    __tablename__ = "divisions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    conference_id: Mapped[int] = mapped_column(
        ForeignKey("conferences.id"), index=True, nullable=False
    )

    conference: Mapped["Conference"] = relationship(
        "Conference", back_populates="divisions"
    )
    teams: Mapped[list["Team"]] = relationship("Team", back_populates="division")
