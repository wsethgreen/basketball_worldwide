from typing import Any, Mapping, Sequence
from uuid import UUID

from sqlalchemy import select

from src.db.models.team_game_stats import TeamGameStats
from src.models.team import TeamGameStatsDto
from src.repositories.base import BaseRepo


class TeamGameStatsRepo(BaseRepo):
    async def get(self, stats_id: UUID) -> TeamGameStats | None:
        return await self.session.get(TeamGameStats, stats_id)

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[TeamGameStats]:
        stmt = select(TeamGameStats)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_for_team(
        self, team_id: int, season_year: int | None = None
    ) -> Sequence[TeamGameStats]:
        stmt = select(TeamGameStats).where(TeamGameStats.team_id == team_id)
        if season_year is not None:
            stmt = stmt.where(TeamGameStats.season_year == season_year)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_stats: TeamGameStatsDto) -> TeamGameStats:
        stats = TeamGameStats(**new_stats.model_dump())
        self.session.add(stats)
        await self.session.commit()
        await self.session.refresh(stats)
        return stats

    async def create_many(
        self, new_stats_list: Sequence[TeamGameStatsDto]
    ) -> Sequence[TeamGameStats]:
        if not new_stats_list:
            return []
        records = [TeamGameStats(**stats.model_dump()) for stats in new_stats_list]
        self.session.add_all(records)
        await self.session.commit()
        return records

    async def update(
        self, stats_id: UUID, update: Mapping[str, Any]
    ) -> TeamGameStats | None:
        stats = await self.get(stats_id)
        if stats is None:
            return None
        for field, value in update.items():
            setattr(stats, field, value)
        await self.session.commit()
        await self.session.refresh(stats)
        return stats

    async def delete(self, stats_id: UUID) -> None:
        stats = await self.get(stats_id)
        if stats is None:
            return None
        await self.session.delete(stats)
        await self.session.commit()
