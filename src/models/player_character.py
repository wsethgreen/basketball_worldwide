from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BasePlayerCharacter(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    title: str = "general_manager"
    play_style: str | None = None
    reputation: int = 50
    team_id: int | None = None


class PlayerCharacterRead(BasePlayerCharacter):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class PlayerCharacterCreate(BasePlayerCharacter):
    pass


class PlayerCharacterUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    title: str | None = None
    play_style: str | None = None
    reputation: int | None = None
    team_id: int | None = None
