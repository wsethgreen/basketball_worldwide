from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ScheduledGameStatus(StrEnum):
    PLAYED = "played"
    SCHEDULED = "scheduled"


class BaseScheduledGame(BaseModel):
    season_year: int
    game_date: date | None = None
    home_team_id: int
    away_team_id: int
    status: ScheduledGameStatus = ScheduledGameStatus.SCHEDULED


class ScheduleGameRead(BaseScheduledGame):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ScheduledGameCreate(BaseScheduledGame):
    pass


class ScheduledGameUpdate(BaseModel):
    game_date: date | None = None
    status: str | None = None
