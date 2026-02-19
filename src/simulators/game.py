import random
from typing import Optional

from src.generators.team import TeamProfile
from src.models.game import GameResult, PossessionEvent


class GameSimulator:
    def __init__(
        self,
        away_team: TeamProfile,
        home_team: TeamProfile,
        possessions: Optional[int] = None,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.away_team = away_team
        self.home_team = home_team
        self.possessions = possessions
        self.rng = rng or random.Random()
        self._validate_team(self.away_team)
        self._validate_team(self.home_team)
        if self.possessions is not None and self.possessions <= 0:
            raise ValueError("possessions must be positive when provided")

    @staticmethod
    def _validate_team(team: TeamProfile) -> None:
        if team.pace <= 0:
            raise ValueError(f"{team.name} pace must be positive")
        for field_name, value in (
            ("turnover_rate", team.turnover_rate),
            ("three_rate", team.three_rate),
            ("two_pct", team.two_pct),
            ("three_pct", team.three_pct),
            ("ft_rate", team.ft_rate),
            ("ft_pct", team.ft_pct),
        ):
            if not 0 <= value <= 1:
                raise ValueError(f"{team.name} {field_name} must be between 0 and 1")

    def _game_possessions(self) -> int:
        if self.possessions is not None:
            return self.possessions

        baseline = self.away_team.pace + self.home_team.pace
        # Add small game-to-game variance (~ +/- 6%).
        variance = self.rng.uniform(-0.06, 0.06)
        total = int(round(baseline * (1 + variance)))
        return max(1, total)

    def _simulate_possession(self, team: TeamProfile) -> tuple[str, int]:
        if self.rng.random() < team.turnover_rate:
            return "turnover", 0

        if self.rng.random() < team.ft_rate:
            made_fts = 0
            for _ in range(2):
                if self.rng.random() < team.ft_pct:
                    made_fts += 1
            return "free_throws", made_fts * team.points_per_ft

        if self.rng.random() < team.three_rate:
            made = self.rng.random() < team.three_pct
            return (
                "three_made" if made else "three_miss",
                team.points_per_three if made else 0,
            )

        made = self.rng.random() < team.two_pct
        return "two_made" if made else "two_miss", team.points_per_two if made else 0

    def simulate_game(self, log_possessions: bool = False) -> GameResult:
        away_score = 0
        home_score = 0
        total_possessions = self._game_possessions()
        possessions_log: Optional[list[PossessionEvent]] = (
            [] if log_possessions else None
        )

        for possession in range(total_possessions):
            team = self.away_team if possession % 2 == 0 else self.home_team
            outcome, points = self._simulate_possession(team)
            if team is self.away_team:
                away_score += points
            else:
                home_score += points
            if possessions_log is not None:
                possessions_log.append(
                    PossessionEvent(
                        number=possession + 1,
                        team=team.name,
                        outcome=outcome,
                        points=points,
                    )
                )

        winner: Optional[str]
        if away_score > home_score:
            winner = self.away_team.name
        elif home_score > away_score:
            winner = self.home_team.name
        else:
            winner = None

        return GameResult(
            away_team=self.away_team,
            home_team=self.home_team,
            possessions=total_possessions,
            away_score=away_score,
            home_score=home_score,
            winner=winner,
            possessions_log=possessions_log,
        )

    def simulate_many(self, games: int) -> dict[str, float]:
        if games <= 0:
            raise ValueError("games must be positive")

        wins_a = 0
        wins_b = 0
        ties = 0

        for _ in range(games):
            result = self.simulate_game()
            if result.winner == self.away_team.name:
                wins_a += 1
            elif result.winner == self.home_team.name:
                wins_b += 1
            else:
                ties += 1

        return {
            self.away_team.name: wins_a / games,
            self.home_team.name: wins_b / games,
            "tie": ties / games,
        }
