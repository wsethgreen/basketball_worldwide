from typing import Sequence

from src.models.player import PlayerDto
from src.models.team import TeamProfile
from src.models.simulate import SimulateGameResponse
from src.simulators.game import GameSimulator


class SimService:
    def __init__(
        self,
        away_team_profile: TeamProfile,
        home_team_profile: TeamProfile,
        away_roster: Sequence[PlayerDto],
        home_roster: Sequence[PlayerDto],
    ):
        self.away_team_profile = away_team_profile
        self.home_team_profile = home_team_profile
        self.game_simulator = GameSimulator(
            away_team=away_team_profile,
            home_team=home_team_profile,
            away_roster=away_roster,
            home_roster=home_roster,
        )

    async def sim_game(self) -> SimulateGameResponse:
        result = self.game_simulator.simulate_game()

        return SimulateGameResponse(
            away_team=self.away_team_profile.name,
            home_team=self.home_team_profile.name,
            away_score=result.away_score,
            home_score=result.home_score,
            winner=result.winner,
            possessions=result.possessions,
            away_player_stats=result.away_player_stats or [],
            home_player_stats=result.home_player_stats or [],
        )

    async def sim_many(self, number_game: int) -> dict:
        result = self.game_simulator.simulate_many(number_game)
        return result
