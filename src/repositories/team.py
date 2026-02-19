from typing import Sequence

from sqlalchemy import select

from src.db.models.team import Team
from src.models.team import TeamCreate, TeamUpdate
from src.repositories.base import BaseRepo


class TeamRepo(BaseRepo):
    async def get(self, team_id: int) -> Team | None:
        return await self.session.get(Team, team_id)

    async def get_teams_for_league(self, league_id: int) -> Sequence[Team]:
        statement = select(Team).where(Team.league_id == league_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_teams_by_ids(self, team_ids: Sequence[int]) -> Sequence[Team]:
        if not team_ids:
            return []
        statement = select(Team).where(Team.id.in_(team_ids))
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[Team]:
        stmt = select(Team)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_team: TeamCreate) -> Team:
        data = new_team.model_dump()
        team = Team(**data)
        self.session.add(team)
        await self.session.commit()
        await self.session.refresh(team)
        return team

    async def update(self, team_id: int, update: TeamUpdate) -> Team | None:
        team = await self.get(team_id)
        if team is None:
            return None
        data = update.model_dump()
        for field, value in data.items():
            setattr(team, field, value)
        await self.session.commit()
        await self.session.refresh(team)
        return team

    async def delete(self, team_id: int) -> None:
        team = await self.get(team_id)
        if team is None:
            return None
        await self.session.delete(team)
        await self.session.commit()
