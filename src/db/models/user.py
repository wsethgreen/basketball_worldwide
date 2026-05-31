from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.player_character import PlayerCharacter


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    display_name: Mapped[str]
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String, nullable=True)

    primary_platform: Mapped[str | None] = mapped_column(String, nullable=True)
    last_login_platform: Mapped[str | None] = mapped_column(String, nullable=True)
    user_device_id: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True
    )

    steam_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    steam_username: Mapped[str | None] = mapped_column(String, nullable=True)
    xbox_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    xbox_gamertag: Mapped[str | None] = mapped_column(String, nullable=True)
    psn_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    psn_username: Mapped[str | None] = mapped_column(String, nullable=True)
    epic_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    epic_username: Mapped[str | None] = mapped_column(String, nullable=True)
    nintendo_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    nintendo_username: Mapped[str | None] = mapped_column(String, nullable=True)

    preferred_locale: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    player_characters: Mapped[list["PlayerCharacter"]] = relationship(
        "PlayerCharacter",
        back_populates="user",
        cascade="all, delete-orphan",
    )
