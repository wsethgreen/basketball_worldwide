from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.generators.team import TeamGenerator
from src.models.player import PlayerDto
from src.repositories.player import PlayerRepo
from src.repositories.team import TeamRepo
from src.simulators.game import GameSimulator


class SimService:
    def __init__(self, session: AsyncSession):
        self.player_repo = PlayerRepo(session=session)
        self.team_repo = TeamRepo(session=session)
        self.team_generator = TeamGenerator()

    async def sim_game(self, away_team_id: int, home_team_id: int):
        teams = await self.team_repo.get_teams_by_ids([away_team_id, home_team_id])

        away_team = next(
            (team for team in teams if team.id == away_team_id),
            None,
        )
        if not away_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Away team with id {away_team_id} not found",
            )

        home_team = next((team for team in teams if team.id == home_team_id), None)

        if not home_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Home team with id {home_team_id} not found",
            )

        away_roster = await self._get_players_for_team(team_id=away_team.id)
        home_roster = await self._get_players_for_team(team_id=home_team.id)

        away_team_profile = self.team_generator.build_team_profile_from_roster(
            city=away_team.city,
            nickname=away_team.nickname,
            roster=away_roster,
        )
        home_team_profile = self.team_generator.build_team_profile_from_roster(
            city=home_team.city,
            nickname=home_team.nickname,
            roster=home_roster,
        )

        game_simulator = GameSimulator(
            away_team=away_team_profile, home_team=home_team_profile
        )
        result = game_simulator.simulate_game()

        return {
            "away_team": away_team_profile.name,
            "home_team": home_team_profile.name,
            "away_score": result.away_score,
            "home_score": result.home_score,
            "winner": result.winner,
            "possessions": result.possessions,
        }

    async def _get_players_for_team(self, team_id: int) -> list[PlayerDto]:
        players = await self.player_repo.get_players_for_team(team_id=team_id)

        if not players:
            raise HTTPException(
                status_code=404, detail=f"Roster not found for team with id: {team_id}"
            )

        return [
            PlayerDto.model_validate(player, from_attributes=True) for player in players
        ]
