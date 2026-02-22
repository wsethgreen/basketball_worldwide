from pydantic import BaseModel, ConfigDict

from src.models.conference import ConferenceRead


class BaseLeague(BaseModel):
    name: str


class LeagueRead(BaseLeague):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conferences: list[ConferenceRead] = []


class LeagueCreate(BaseLeague):
    pass


class LeagueUpdate(BaseLeague):
    pass
