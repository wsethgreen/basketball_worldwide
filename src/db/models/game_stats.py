from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.player import Player


class GameStats(Base):
    __tablename__ = "game_stats"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    player_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("players.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    minutes: Mapped[int]
    points: Mapped[int]
    fg_attempted: Mapped[int]
    fg_made: Mapped[int]
    three_point_attempted: Mapped[int]
    three_point_made: Mapped[int]
    ft_attempted: Mapped[int]
    ft_made: Mapped[int]
    fg_percent: Mapped[float]
    three_point_percent: Mapped[float]
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

    player: Mapped["Player"] = relationship("Player", back_populates="game_stats")
