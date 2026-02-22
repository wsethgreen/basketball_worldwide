from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.player_game_stats import PlayerGameStats
    from src.db.models.player_attributes import PlayerAttributes


class Player(Base):
    __tablename__ = "players"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    first_name: Mapped[str]
    last_name: Mapped[str]
    age: Mapped[int]
    height: Mapped[float]
    archetype: Mapped[str]
    # caliber: Mapped[str]
    positions: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )

    attributes: Mapped["PlayerAttributes"] = relationship(
        "PlayerAttributes",
        back_populates="player",
        uselist=False,
    )
    game_stats: Mapped[list["PlayerGameStats"]] = relationship(
        "PlayerGameStats",
        back_populates="player",
        cascade="all, delete-orphan",
    )
