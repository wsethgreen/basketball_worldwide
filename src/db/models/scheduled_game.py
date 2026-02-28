from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class ScheduledGame(Base):
    __tablename__ = "scheduled_games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season_year: Mapped[int]
    game_date: Mapped[date | None] = mapped_column(
        default=None
    )  # Should this be datetime to track game start time?
    status: Mapped[str] = mapped_column(String(20), default="scheduled")
    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )

    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
