from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str]
    nickname: Mapped[str]
    budget: Mapped[int | None] = mapped_column()
    league_id: Mapped[int] = mapped_column(
        ForeignKey("leagues.id"), index=True, nullable=False
    )

    league = relationship("League", back_populates="teams")
