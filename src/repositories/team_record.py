from typing import Sequence

from sqlalchemy import select

from src.db.models.team_record import TeamRecord
from src.repositories.base import BaseRepo


class TeamRecordRepo(BaseRepo):
    async def get(self, record_id: int) -> TeamRecord | None:
        return await self.session.get(TeamRecord, record_id)

    async def get_for_team(self, team_id: int) -> TeamRecord | None:
        stmt = select(TeamRecord).where(TeamRecord.team_id == team_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[TeamRecord]:
        stmt = select(TeamRecord)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, team_id: int, year: int) -> TeamRecord:
        record = TeamRecord(team_id=team_id, wins=0, losses=0, year=year)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def update(self, record: TeamRecord) -> TeamRecord:
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def increment(self, team_id: int, won: bool) -> TeamRecord:
        record = await self.get_for_team(team_id=team_id)

        if won:
            record.wins + 1
        else:
            record.losses + 1

        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def update_by_team_id(self, team_id: int, won: bool) -> TeamRecord:
        record = await self.get_for_team(team_id)
        if record is None:
            record = await self.create(team_id)
        if won:
            record.wins += 1
        else:
            record.losses += 1
        return await self.update(record)

    async def delete(self, team_record_id: int) -> None:
        stats = await self.get(team_record_id)
        if stats is None:
            return None
        await self.session.delete(stats)
        await self.session.commit()
