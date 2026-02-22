from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.division import Division
    from src.db.models.league import League


class Conference(Base):
    __tablename__ = "conferences"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    league_id: Mapped[int] = mapped_column(
        ForeignKey("leagues.id"), index=True, nullable=False
    )

    league: Mapped["League"] = relationship("League", back_populates="conferences")
    divisions: Mapped[list["Division"]] = relationship(
        "Division", back_populates="conference"
    )
