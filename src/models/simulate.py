from pydantic import BaseModel


class SimulateGameRequest(BaseModel):
    away_team_id: int
    home_team_id: int


class SimulateGameResponse(BaseModel):
    away_team: str
    home_team: str
    away_score: int
    home_score: int
    winner: str | None
    possessions: int
