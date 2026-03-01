from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class TeamRecord(Base):
    __tablename__ = "team_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )
    wins: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    year: Mapped[int]

    team = relationship("Team")
