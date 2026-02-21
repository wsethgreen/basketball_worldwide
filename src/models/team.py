from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict

from src.models.player import PlayerDto


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


class TeamGenerateRoster(BaseModel):
    generate_new: bool = False


class TeamUpdate(BaseModel):
    city: str
    nickname: str
    budget: int | None


@dataclass(frozen=True)
class TeamProfile:
    name: str
    pace: float
    turnover_rate: float
    three_rate: float
    two_pct: float
    three_pct: float
    ft_rate: float
    ft_pct: float
    points_per_two: int = 2
    points_per_three: int = 3
    points_per_ft: int = 1


class TeamProfiles(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    away_team_profile: TeamProfile
    home_team_profile: TeamProfile
    away_roster: list[PlayerDto]
    home_roster: list[PlayerDto]
