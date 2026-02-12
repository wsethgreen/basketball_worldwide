from pydantic import BaseModel, ConfigDict


class BaseTeam(BaseModel):
    id: int
    city: str
    nickname: str
    budget: int | None
    league_id: int


class TeamRead(BaseTeam):
    model_config = ConfigDict(from_attributes=True)


class TeamCreate(BaseModel):
    league_id: int
    city: str
    nickname: str
    budget: int | None
    league_id: int


class TeamUpdate(BaseModel):
    city: str
    nickname: str
    budget: int | None
