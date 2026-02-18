from pydantic import BaseModel


class SimulateGameRequest(BaseModel):
    away_team_id: int
    home_team_id: int
