from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.player import PlayerDto


class BaseTeam(BaseModel):
    id: int
    city: str
    nickname: str
    budget: int | None
    division_id: int


class TeamRead(BaseTeam):
    model_config = ConfigDict(from_attributes=True)


class TeamCreate(BaseModel):
    city: str
    nickname: str
    budget: int | None
    division_id: int


class TeamGenerateRoster(BaseModel):
    generate_new: bool = False


class TeamUpdate(BaseModel):
    city: str
    nickname: str
    budget: int | None
    division_id: int


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


class TeamGameStatsDto(BaseModel):
    id: UUID | None = None
    team_id: int
    game_id: UUID
    season_year: int
    points: int = 0
    fg_attempted: int = 0
    fg_made: int = 0
    three_point_attempted: int = 0
    three_point_made: int = 0
    ft_attempted: int = 0
    ft_made: int = 0
    off_rebounds: int = 0
    def_rebounds: int = 0
    rebounds: int = 0
    assists: int = 0
    turnovers: int = 0
    steals: int = 0
    blocks: int = 0
    personal_fouls: int = 0
    technical_fouls: int = 0
    plus_minus: int = 0
