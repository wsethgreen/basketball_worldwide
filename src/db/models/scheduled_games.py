from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class ScheduledGames(Base):
    __tablename__ = "scheduled_games"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
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
