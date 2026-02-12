from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.schemas.base import Base

if TYPE_CHECKING:
    from src.db.schemas.team import Team


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    teams: Mapped[list["Team"]] = relationship("Team", back_populates="league")
