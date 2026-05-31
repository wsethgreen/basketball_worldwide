from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.team import Team


class PlayerCharacter(Base):
    __tablename__ = "player_characters"
    __table_args__ = (
        CheckConstraint(
            "reputation >= 0 AND reputation <= 100",
            name="ck_player_characters_reputation_range",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    title: Mapped[str] = mapped_column(String, default="general_manager")
    play_style: Mapped[str | None] = mapped_column(String, nullable=True)
    reputation: Mapped[int] = mapped_column(default=50)
    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=True, unique=True
    )

    team: Mapped["Team | None"] = relationship(
        "Team",
        back_populates="player_character",
    )
