from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.player import Player


class PlayerAttributes(Base):
    __tablename__ = "player_attributes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    player_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("players.id", ondelete="CASCADE"),
        index=True,
    )
    # physical
    speed: Mapped[int]
    agility: Mapped[int]
    strength: Mapped[int]
    stamina: Mapped[int]
    # vertical: Mapped[int]
    # shooting
    inside_scoring: Mapped[int]
    midrange_scoring: Mapped[int]
    free_throw: Mapped[int]
    three_point: Mapped[int]
    # skill
    ball_handling: Mapped[int]
    passing: Mapped[int]
    # off_ball_movement: Mapped[int]
    # defense
    perimeter_defense: Mapped[int]
    interior_defense: Mapped[int]
    steal: Mapped[int]
    block: Mapped[int]
    # rebounding
    def_rebound: Mapped[int]
    off_rebound: Mapped[int]
    # mental
    iq: Mapped[int]
    clutch: Mapped[int]

    player: Mapped["Player"] = relationship(
        "Player",
        back_populates="attributes",
    )
