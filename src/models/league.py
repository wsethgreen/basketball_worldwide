from pydantic import BaseModel, ConfigDict


class BaseLeague(BaseModel):
    name: str


class LeagueRead(BaseLeague):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LeagueCreate(BaseLeague):
    pass


class LeagueUpdate(BaseLeague):
    pass
