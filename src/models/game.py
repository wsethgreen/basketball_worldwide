from dataclasses import dataclass
from uuid import UUID

from src.models.team import TeamProfile


@dataclass(frozen=True)
class PossessionEvent:
    number: int
    team: str
    outcome: str
    points: int


@dataclass(frozen=True)
class PossessionResult:
    outcome: str
    points: int
    shot_type: str | None = None
    shot_made: bool | None = None
    ft_attempts: int = 0
    ft_made: int = 0
    turnover: bool = False
    shooter_id: UUID | None = None
    turnover_player_id: UUID | None = None


@dataclass
class PlayerGameStats:
    player_id: UUID
    first_name: str
    last_name: str
    points: int = 0
    fg_attempted: int = 0
    fg_made: int = 0
    three_point_attempted: int = 0
    three_point_made: int = 0
    ft_attempted: int = 0
    ft_made: int = 0
    off_rebounds: int = 0
    def_rebounds: int = 0
    assists: int = 0
    turnovers: int = 0


@dataclass(frozen=True)
class GameResult:
    away_team: TeamProfile
    home_team: TeamProfile
    possessions: int
    away_score: int
    home_score: int
    winner: str | None
    possessions_log: list[PossessionEvent] | None = None
    away_player_stats: list[PlayerGameStats] | None = None
    home_player_stats: list[PlayerGameStats] | None = None
