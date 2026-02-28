import random

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.generators.division import DivisionGenerator
from src.generators.schedule import ScheduleGenerator
from src.models.conference import ConferenceCreate
from src.models.division import DivisionCreate
from src.models.league import LeagueCreate
from src.repositories.conference import ConferenceRepo
from src.repositories.division import DivisionRepo
from src.repositories.league import LeagueRepo
from src.repositories.scheduled_game import ScheduledGameRepo
from src.repositories.team import TeamRepo


class LeagueService:
    def __init__(self, session: AsyncSession):
        self.league_repo = LeagueRepo(session=session)
        self.conference_repo = ConferenceRepo(session=session)
        self.division_repo = DivisionRepo(session=session)
        self.scheduled_game_repo = ScheduledGameRepo(session=session)
        self.team_repo = TeamRepo(session=session)
        self.division_generator = DivisionGenerator()
        self.schedule_generator = ScheduleGenerator()

    async def create_league(self, league_in: LeagueCreate):
        prefix = random.choice(["Pro", "Elite", "Premier"])
        sport = random.choice(["Basketball", "Hoops", "Roundball"])
        suffix = random.choice(["League", "Association", "Federation"])
        new_league = LeagueCreate(name=f"{prefix} {sport} {suffix}")
        league = await self.league_repo.create(new_league)

        conference_names = ["East", "West"]
        division_names = self.division_generator.generate_names(8)
        for index, conf_name in enumerate(conference_names):
            conference = await self.conference_repo.create(
                ConferenceCreate(name=conf_name, league_id=league.id)
            )
            for name in division_names[index * 4 : (index + 1) * 4]:
                await self.division_repo.create(
                    DivisionCreate(name=name, conference_id=conference.id)
                )

        return await self.league_repo.get(league.id)

    async def get_league(self, league_id: int):
        league = await self.league_repo.get(league_id)
        if league is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="League not found"
            )
        return league

    async def get_teams_for_league(self, league_id: int):
        return await self.team_repo.get_teams_for_league(league_id)

    async def generate_schedule_for_league(
        self, league_id: int, season_year: int, batch_size: int = 100
    ) -> int:
        teams = await self.team_repo.get_teams_for_league(league_id)
        divisions = await self.division_repo.get_divisions_for_league(league_id)
        games = self.schedule_generator.generate(
            teams=teams, divisions=divisions, season_year=season_year
        )

        for i in range(0, len(games), batch_size):
            batch = games[i : i + batch_size]
            await self.scheduled_game_repo.create_many(batch)

        return len(games)

    async def delete_schedule_for_league(self, league_id: int, season_year: int) -> int:
        return await self.scheduled_game_repo.delete_for_league_season(
            league_id, season_year
        )
