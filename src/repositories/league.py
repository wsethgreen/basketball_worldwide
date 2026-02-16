from __future__ import annotations

from typing import Sequence

from sqlalchemy import select

from src.db.models.league import League
from src.models.league import LeagueCreate, LeagueUpdate
from src.repositories.base import BaseRepo


class LeagueRepo(BaseRepo):
    async def get(self, league_id: int) -> League | None:
        return await self.session.get(League, league_id)

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[League]:
        stmt = select(League)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_league: LeagueCreate) -> League:
        data = new_league.model_dump()
        league = League(**data)
        self.session.add(league)
        await self.session.commit()
        await self.session.refresh(league)
        return league

    async def update(self, league_id: int, update: LeagueUpdate) -> League | None:
        league = await self.get(league_id)
        if league is None:
            return None
        data = update.model_dump()
        for field, value in data.items():
            setattr(league, field, value)
        await self.session.commit()
        await self.session.refresh(league)
        return league

    async def delete(self, league_id: int) -> None:
        league = await self.get(league_id)
        if league is None:
            return None
        await self.session.delete(league)
        await self.session.commit()
