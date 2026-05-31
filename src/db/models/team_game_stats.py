from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class TeamGameStats(Base):
    __tablename__ = "team_game_stats"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )
    game_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("scheduled_games.id"),
        index=True,
        nullable=False,
    )
    season_year: Mapped[int]
    points: Mapped[int]
    fg_attempted: Mapped[int]
    fg_made: Mapped[int]
    three_point_attempted: Mapped[int]
    three_point_made: Mapped[int]
    ft_attempted: Mapped[int]
    ft_made: Mapped[int]
    off_rebounds: Mapped[int]
    def_rebounds: Mapped[int]
    rebounds: Mapped[int]
    assists: Mapped[int]
    turnovers: Mapped[int]
    steals: Mapped[int]
    blocks: Mapped[int]
    personal_fouls: Mapped[int]
    technical_fouls: Mapped[int]
    plus_minus: Mapped[int]

    team = relationship("Team")
    game = relationship("ScheduledGames")
