from pydantic import BaseModel, ConfigDict

from src.models.division import DivisionRead


class BaseConference(BaseModel):
    name: str
    league_id: int


class ConferenceRead(BaseConference):
    model_config = ConfigDict(from_attributes=True)
    id: int
    divisions: list[DivisionRead] = []


class ConferenceCreate(BaseConference):
    pass


class ConferenceUpdate(BaseModel):
    name: str
