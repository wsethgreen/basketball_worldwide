from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from src.db.models.player_game_stats import PlayerGameStats
from src.models.player import PlayerGameStatsCreate
from src.repositories.base import BaseRepo


class PlayerGameStatsRepo(BaseRepo):
    async def get(self, stats_id: UUID) -> PlayerGameStats | None:
        return await self.session.get(PlayerGameStats, stats_id)

    async def get_player_game_stats(self, player_id: UUID) -> Sequence[PlayerGameStats]:
        stmt = select(PlayerGameStats).where(PlayerGameStats.player_id == player_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[PlayerGameStats]:
        stmt = select(PlayerGameStats)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_stats: PlayerGameStatsCreate) -> PlayerGameStats:
        data = new_stats.model_dump()
        stats = PlayerGameStats(**data)
        self.session.add(stats)
        await self.session.commit()
        await self.session.refresh(stats)
        return stats

    async def create_many(
        self, game_stats: Sequence[PlayerGameStatsCreate]
    ) -> Sequence[PlayerGameStats]:
        if not game_stats:
            return []
        stats_records = [PlayerGameStats(**stats.model_dump()) for stats in game_stats]
        self.session.add_all(stats_records)
        await self.session.commit()
        for record in stats_records:
            await self.session.refresh(record)
        return stats_records

    async def update(
        self, stats_id: UUID, update: PlayerGameStats
    ) -> PlayerGameStats | None:
        stats = await self.get(stats_id)
        if stats is None:
            return None
        data = update.__dict__
        for field, value in data.items():
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
