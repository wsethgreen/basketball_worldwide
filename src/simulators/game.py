from __future__ import annotations

import random
from typing import Optional, Sequence, Any
from uuid import UUID

from src.models.game import (
    GameResult,
    PlayerGameStats,
    PossessionEvent,
    PossessionOutcome,
)
from src.models.player import PlayerDto
from src.models.team import TeamProfile


class GameSimulator:
    def __init__(
        self,
        away_team: TeamProfile,
        home_team: TeamProfile,
        away_roster: Sequence[PlayerDto],
        home_roster: Sequence[PlayerDto],
        possessions: int | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self.away_team = away_team
        self.home_team = home_team
        self.away_roster = away_roster
        self.home_roster = home_roster
        self.possessions = possessions
        self.rng = rng or random.Random()

    def _game_possessions(self) -> int:
        if self.possessions is not None:
            return self.possessions

        baseline = self.away_team.pace + self.home_team.pace
        # Add small game-to-game variance (~ +/- 6%).
        variance = self.rng.uniform(-0.06, 0.06)
        total = int(round(baseline * (1 + variance)))
        return max(1, total)

    def _simulate_possession(self, team: TeamProfile) -> PossessionOutcome:
        if self.rng.random() < team.turnover_rate:
            return PossessionOutcome(outcome="turnover", points=0, turnover=True)

        elif self.rng.random() < team.ft_rate:
            made_fts = 0
            for _ in range(2):
                if self.rng.random() < team.ft_pct:
                    made_fts += 1
            return PossessionOutcome(
                outcome="free_throws",
                points=made_fts * team.points_per_ft,
                ft_attempts=2,
                ft_made=made_fts,
            )

        elif self.rng.random() < team.three_rate:
            made = self.rng.random() < team.three_pct
            return PossessionOutcome(
                outcome="three_made" if made else "three_miss",
                points=team.points_per_three if made else 0,
                shot_type="three",
                shot_made=made,
            )
        else:
            made = self.rng.random() < team.two_pct
            return PossessionOutcome(
                outcome="two_made" if made else "two_miss",
                points=team.points_per_two if made else 0,
                shot_type="two",
                shot_made=made,
            )

    @staticmethod
    def _init_player_stats(roster: Sequence[PlayerDto]) -> dict[UUID, PlayerGameStats]:
        return {
            player.id: PlayerGameStats(
                player_id=player.id,
                first_name=player.first_name,
                last_name=player.last_name,
            )
            for player in roster
        }

    def _weighted_choice(self, roster: Sequence[PlayerDto], weight_fn) -> PlayerDto:
        roster_list = list(roster)
        weights = [max(1.0, float(weight_fn(player))) for player in roster_list]
        total = sum(weights)
        if total <= 0:
            return self.rng.choice(roster_list)
        roll = self.rng.uniform(0, total)
        upto = 0.0
        for player, weight in zip(roster_list, weights):
            upto += weight
            if upto >= roll:
                return player
        return roster_list[-1]

    def _select_shooter(self, roster: Sequence[PlayerDto], shot_type: str) -> PlayerDto:
        if shot_type == "three":
            return self._weighted_choice(roster, lambda p: p.attributes.three_point)
        return self._weighted_choice(
            roster,
            lambda p: (
                (p.attributes.inside_scoring * 0.6)
                + (p.attributes.midrange_scoring * 0.4)
            ),
        )

    def _select_turnover_player(self, roster: Sequence[PlayerDto]) -> PlayerDto:
        return self._weighted_choice(
            roster,
            lambda p: (
                (100 - p.attributes.ball_handling) * 0.7
                + (100 - p.attributes.passing) * 0.3
            ),
        )

    def _select_assist_player(
        self, roster: Sequence[PlayerDto], shooter_id: UUID
    ) -> PlayerDto | None:
        candidates = [p for p in roster if p.id != shooter_id]
        if not candidates:
            return None
        return self._weighted_choice(candidates, lambda p: p.attributes.passing)

    def _select_rebounder(
        self,
        offense_roster: Sequence[PlayerDto],
        defense_roster: Sequence[PlayerDto],
    ) -> tuple[PlayerDto, bool]:
        off_total = sum(p.attributes.off_rebound for p in offense_roster)
        def_total = sum(p.attributes.def_rebound for p in defense_roster)
        if off_total + def_total <= 0:
            return self.rng.choice(list(defense_roster)), False
        off_prob = off_total / (off_total + def_total)
        if self.rng.random() < off_prob:
            return (
                self._weighted_choice(
                    offense_roster, lambda p: p.attributes.off_rebound
                ),
                True,
            )
        return (
            self._weighted_choice(defense_roster, lambda p: p.attributes.def_rebound),
            False,
        )

    def _apply_possession_stats(
        self,
        outcome: PossessionOutcome,
        roster: Sequence[PlayerDto],
        stats_map: dict[UUID, PlayerGameStats],
        opponent_roster: Sequence[PlayerDto],
        opponent_stats_map: dict[UUID, PlayerGameStats],
    ) -> None:
        if outcome.turnover:
            turnover_player = self._select_turnover_player(roster)
            stats_map[turnover_player.id].turnovers += 1
            return

        if outcome.ft_attempts:
            shooter = self._weighted_choice(roster, lambda p: p.attributes.free_throw)
            stats = stats_map[shooter.id]
            stats.ft_attempted += outcome.ft_attempts
            stats.ft_made += outcome.ft_made
            stats.points += outcome.points
            return

        if outcome.shot_type is None:
            return

        shooter = self._select_shooter(roster, outcome.shot_type)
        stats = stats_map[shooter.id]
        stats.fg_attempted += 1
        if outcome.shot_made:
            stats.fg_made += 1
        if outcome.shot_type == "three":
            stats.three_point_attempted += 1
            if outcome.shot_made:
                stats.three_point_made += 1
        stats.points += outcome.points

        if outcome.shot_made:
            if self.rng.random() < 0.5:
                assister = self._select_assist_player(roster, shooter.id)
                if assister is not None:
                    stats_map[assister.id].assists += 1
            return

        rebounder, offensive = self._select_rebounder(roster, opponent_roster)
        if offensive:
            stats_map[rebounder.id].off_rebounds += 1
        else:
            opponent_stats_map[rebounder.id].def_rebounds += 1

    def simulate_game(self, log_possessions: bool = False) -> GameResult:
        away_score = 0
        home_score = 0
        total_possessions = self._game_possessions()
        possessions_log: Optional[list[PossessionEvent]] = (
            [] if log_possessions else None
        )
        away_stats_map = (
            self._init_player_stats(self.away_roster)
            if self.away_roster is not None
            else None
        )
        home_stats_map = (
            self._init_player_stats(self.home_roster)
            if self.home_roster is not None
            else None
        )

        for possession in range(total_possessions):
            team = self.away_team if possession % 2 == 0 else self.home_team
            outcome = self._simulate_possession(team)
            if team is self.away_team:
                away_score += outcome.points
            else:
                home_score += outcome.points
            if (
                away_stats_map is not None
                and home_stats_map is not None
                and self.away_roster is not None
                and self.home_roster is not None
            ):
                if team is self.away_team:
                    self._apply_possession_stats(
                        outcome,
                        roster=self.away_roster,
                        stats_map=away_stats_map,
                        opponent_roster=self.home_roster,
                        opponent_stats_map=home_stats_map,
                    )
                else:
                    self._apply_possession_stats(
                        outcome,
                        roster=self.home_roster,
                        stats_map=home_stats_map,
                        opponent_roster=self.away_roster,
                        opponent_stats_map=away_stats_map,
                    )
            if possessions_log is not None:
                possessions_log.append(
                    PossessionEvent(
                        number=possession + 1,
                        team=team.name,
                        outcome=outcome.outcome,
                        points=outcome.points,
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
            away_player_stats=(
                [away_stats_map[p.id] for p in self.away_roster]
                if away_stats_map is not None and self.away_roster is not None
                else None
            ),
            home_player_stats=(
                [home_stats_map[p.id] for p in self.home_roster]
                if home_stats_map is not None and self.home_roster is not None
                else None
            ),
        )

    def simulate_many(self, games: int) -> dict[str, Any]:
        if games <= 0:
            raise ValueError("games must be positive")

        wins_a = 0
        wins_b = 0
        ties = 0
        results: list[GameResult] = []

        for _ in range(games):
            result = self.simulate_game()
            results.append(result)
            if result.winner == self.away_team.name:
                wins_a += 1
            elif result.winner == self.home_team.name:
                wins_b += 1
            else:
                ties += 1

        return {
            "results": [results],
            self.away_team.name: wins_a / games,
            self.home_team.name: wins_b / games,
            "tie": ties / games,
        }
