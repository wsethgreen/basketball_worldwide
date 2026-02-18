from dataclasses import dataclass

from src.models.team import TeamProfile


@dataclass(frozen=True)
class PossessionEvent:
    number: int
    team: str
    outcome: str
    points: int


@dataclass(frozen=True)
class GameResult:
    away_team: TeamProfile
    home_team: TeamProfile
    possessions: int
    away_score: int
    home_score: int
    winner: str | None
    possessions_log: list[PossessionEvent] | None = None
