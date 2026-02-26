import random

from faker import Faker
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.generators.team import TeamGenerator
from src.models.player import PlayerDto
from src.models.team import TeamCreate, TeamProfiles
from src.repositories.division import DivisionRepo
from src.repositories.player import PlayerRepo
from src.repositories.scheduled_game import ScheduledGameRepo
from src.repositories.team import TeamRepo


class TeamService:
    def __init__(self, session: AsyncSession):
        self.player_repo = PlayerRepo(session=session)
        self.team_repo = TeamRepo(session=session)
        self.team_generator = TeamGenerator()
        self.division_repo = DivisionRepo(session=session)
        self.scheduled_game_repo = ScheduledGameRepo(session=session)
        self._faker = Faker()

    async def get_team_profiles(
        self, away_team_id: int, home_team_id: int
    ) -> TeamProfiles:
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

        away_roster = await self.get_roster(team_id=away_team.id)
        home_roster = await self.get_roster(team_id=home_team.id)

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

        return TeamProfiles(
            away_team_profile=away_team_profile,
            home_team_profile=home_team_profile,
            away_roster=away_roster,
            home_roster=home_roster,
        )

    async def create_team(self, team_in: TeamCreate):
        division = await self.division_repo.get(team_in.division_id)
        if division is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Division with id {team_in.division_id} not found",
            )
        nicknames = [
            "Lions",
            "Wolves",
            "Eagles",
            "Hawks",
            "Bulls",
            "Tigers",
            "Falcons",
            "Sharks",
            "Raptors",
            "Panthers",
            "Kings",
            "Storm",
        ]
        new_team = TeamCreate(
            city=self._faker.city(),
            nickname=random.choice(nicknames),
            budget=random.randint(50, 125) * 1_000_000,
            division_id=team_in.division_id,
        )
        return await self.team_repo.create(new_team)

    async def get_roster(self, team_id: int) -> list[PlayerDto]:
        players = await self.player_repo.get_players_for_team(team_id=team_id)

        if not players:
            raise HTTPException(
                status_code=404, detail=f"Roster not found for team with id: {team_id}"
            )

        return [
            PlayerDto.model_validate(player, from_attributes=True) for player in players
        ]

    async def get_schedule(self, team_id: int, season_year: int | None = None):
        return await self.scheduled_game_repo.get_for_team(
            team_id=team_id, season_year=season_year
        )
