from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
import random
from typing import Iterable, Sequence

from src.models.scheduled_game import ScheduledGameCreate


class ScheduleGenerator:
    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()

    def generate(
        self,
        *,
        teams: Sequence,
        divisions: Sequence,
        season_year: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[ScheduledGameCreate]:
        division_to_conference = {d.id: d.conference_id for d in divisions}

        teams_by_division = defaultdict(list)
        teams_by_conference = defaultdict(list)

        for team in teams:
            teams_by_division[team.division_id].append(team)
            conference_id = division_to_conference.get(team.division_id)
            if conference_id is None:
                raise ValueError(
                    f"Division {team.division_id} has no conference mapping"
                )
            teams_by_conference[conference_id].append(team)

        games: list[ScheduledGameCreate] = []

        # In-division: 4 games (2 home, 2 away)
        for division_teams in teams_by_division.values():
            self._add_round_robin_series(
                games,
                division_teams,
                season_year=season_year,
                games_per_pair=4,
            )

        # Same conference, different division: 3 games
        for conference_teams in teams_by_conference.values():
            for i in range(len(conference_teams)):
                for j in range(i + 1, len(conference_teams)):
                    team_a = conference_teams[i]
                    team_b = conference_teams[j]
                    if team_a.division_id == team_b.division_id:
                        continue
                    self._add_series(
                        games,
                        team_a.id,
                        team_b.id,
                        season_year=season_year,
                        games_per_pair=3,
                    )

        # Cross-conference: 2 games (home/away)
        conference_ids = list(teams_by_conference.keys())
        if len(conference_ids) >= 2:
            for i in range(len(conference_ids)):
                for j in range(i + 1, len(conference_ids)):
                    teams_a = teams_by_conference[conference_ids[i]]
                    teams_b = teams_by_conference[conference_ids[j]]
                    for team_a in teams_a:
                        for team_b in teams_b:
                            self._add_series(
                                games,
                                team_a.id,
                                team_b.id,
                                season_year=season_year,
                                games_per_pair=2,
                            )

        if start_date is None:
            start_date = date(season_year, 1, 1)
        if end_date is None:
            end_date = date(season_year, 7, 1)
        self._assign_dates(games, start_date, end_date)

        return games

    def _add_round_robin_series(
        self,
        games: list[ScheduledGameCreate],
        teams: Iterable,
        *,
        season_year: int,
        games_per_pair: int,
    ) -> None:
        teams_list = list(teams)
        for i in range(len(teams_list)):
            for j in range(i + 1, len(teams_list)):
                self._add_series(
                    games,
                    teams_list[i].id,
                    teams_list[j].id,
                    season_year=season_year,
                    games_per_pair=games_per_pair,
                )

    def _add_series(
        self,
        games: list[ScheduledGameCreate],
        team_a_id: int,
        team_b_id: int,
        *,
        season_year: int,
        games_per_pair: int,
    ) -> None:
        if games_per_pair == 2:
            self._add_game(games, season_year, team_a_id, team_b_id)
            self._add_game(games, season_year, team_b_id, team_a_id)
            return

        if games_per_pair == 4:
            for _ in range(2):
                self._add_game(games, season_year, team_a_id, team_b_id)
                self._add_game(games, season_year, team_b_id, team_a_id)
            return

        if games_per_pair == 3:
            # One home each, plus one extra home for a random team to balance overall.
            self._add_game(games, season_year, team_a_id, team_b_id)
            self._add_game(games, season_year, team_b_id, team_a_id)
            extra_home = team_a_id if self.rng.random() < 0.5 else team_b_id
            extra_away = team_b_id if extra_home == team_a_id else team_a_id
            self._add_game(games, season_year, extra_home, extra_away)
            return

        raise ValueError(f"Unsupported games_per_pair: {games_per_pair}")

    @staticmethod
    def _add_game(
        games: list[ScheduledGameCreate],
        season_year: int,
        home_team_id: int,
        away_team_id: int,
    ) -> None:
        games.append(
            ScheduledGameCreate(
                season_year=season_year,
                home_team_id=home_team_id,
                away_team_id=away_team_id,
            )
        )

    def _assign_dates(
        self,
        games: list[ScheduledGameCreate],
        start_date: date,
        end_date: date,
    ) -> None:
        remaining = list(games)
        team_ids = {g.home_team_id for g in remaining} | {
            g.away_team_id for g in remaining
        }
        team_dates: dict[int, set[date]] = {team_id: set() for team_id in team_ids}
        team_week_counts = {team_id: defaultdict(int) for team_id in team_ids}

        total_days = (end_date - start_date).days + 1
        if total_days <= 0:
            raise ValueError("end_date must be on or after start_date")
        avg_games_per_day = len(remaining) / total_days

        current_date = start_date
        while current_date <= end_date and remaining:
            week_key = current_date.isocalendar()[:2]

            days_left = (end_date - current_date).days + 1
            required_daily = (len(remaining) + days_left - 1) // days_left
            daily_target = max(
                0,
                round(max(avg_games_per_day, required_daily) + self.rng.uniform(-1, 1)),
            )

            candidates = []
            for game in remaining:
                if not self._team_can_play(team_dates[game.home_team_id], current_date):
                    continue
                if not self._team_can_play(team_dates[game.away_team_id], current_date):
                    continue
                home_week = team_week_counts[game.home_team_id][week_key]
                away_week = team_week_counts[game.away_team_id][week_key]
                if home_week >= 5 or away_week >= 5:
                    continue
                candidates.append((home_week + away_week, game))

            candidates.sort(key=lambda item: item[0])

            games_scheduled = 0
            for _, game in candidates:
                if games_scheduled >= daily_target:
                    break
                if not self._team_can_play(team_dates[game.home_team_id], current_date):
                    continue
                if not self._team_can_play(team_dates[game.away_team_id], current_date):
                    continue

                game.game_date = current_date
                team_dates[game.home_team_id].add(current_date)
                team_dates[game.away_team_id].add(current_date)
                team_week_counts[game.home_team_id][week_key] += 1
                team_week_counts[game.away_team_id][week_key] += 1
                remaining.remove(game)
                games_scheduled += 1

            current_date += timedelta(days=1)

        if remaining:
            self._relaxed_fill(
                remaining=remaining,
                team_dates=team_dates,
                team_week_counts=team_week_counts,
                start_date=start_date,
                end_date=end_date,
            )

        if remaining:
            raise ValueError(
                f"Unable to schedule all games by {end_date.isoformat()}: "
                f"{len(remaining)} games left"
            )

    @staticmethod
    def _team_can_play(team_dates: set[date], current_date: date) -> bool:
        if current_date in team_dates:
            return False
        return not (
            (current_date - timedelta(days=1) in team_dates)
            and (current_date - timedelta(days=2) in team_dates)
        )

    def _relaxed_fill(
        self,
        *,
        remaining: list[ScheduledGameCreate],
        team_dates: dict[int, set[date]],
        team_week_counts: dict[int, defaultdict],
        start_date: date,
        end_date: date,
    ) -> None:
        current_date = start_date
        while current_date <= end_date and remaining:
            week_key = current_date.isocalendar()[:2]
            self.rng.shuffle(remaining)
            daily_target = (len(remaining) + (end_date - current_date).days) // max(
                1, (end_date - current_date).days + 1
            )
            games_scheduled = 0
            for game in list(remaining):
                if games_scheduled >= daily_target:
                    break
                if not self._team_can_play(team_dates[game.home_team_id], current_date):
                    continue
                if not self._team_can_play(team_dates[game.away_team_id], current_date):
                    continue
                if team_week_counts[game.home_team_id][week_key] >= 6:
                    continue
                if team_week_counts[game.away_team_id][week_key] >= 6:
                    continue
                game.game_date = current_date
                team_dates[game.home_team_id].add(current_date)
                team_dates[game.away_team_id].add(current_date)
                team_week_counts[game.home_team_id][week_key] += 1
                team_week_counts[game.away_team_id][week_key] += 1
                remaining.remove(game)
                games_scheduled += 1

            current_date += timedelta(days=1)
