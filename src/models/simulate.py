from pydantic import BaseModel, ConfigDict

from src.models.game import PlayerGameStats


class SimulateGameRequest(BaseModel):
    away_team_id: int
    home_team_id: int


class SimulateGameResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    away_team: str
    home_team: str
    away_score: int
    home_score: int
    winner: str | None
    possessions: int
    away_player_stats: list[PlayerGameStats]
    home_player_stats: list[PlayerGameStats]
