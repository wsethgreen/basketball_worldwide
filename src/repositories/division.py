from typing import Sequence

from sqlalchemy import select

from src.db.models.conference import Conference
from src.db.models.division import Division
from src.models.division import DivisionCreate, DivisionUpdate
from src.repositories.base import BaseRepo


class DivisionRepo(BaseRepo):
    async def get(self, division_id: int) -> Division | None:
        return await self.session.get(Division, division_id)

    async def get_divisions_for_conference(
        self, conference_id: int
    ) -> Sequence[Division]:
        statement = select(Division).where(Division.conference_id == conference_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_divisions_for_league(self, league_id: int) -> Sequence[Division]:
        statement = (
            select(Division)
            .join(Conference, Division.conference_id == Conference.id)
            .where(Conference.league_id == league_id)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[Division]:
        stmt = select(Division)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_division: DivisionCreate) -> Division:
        data = new_division.model_dump()
        division = Division(**data)
        self.session.add(division)
        await self.session.commit()
        await self.session.refresh(division)
        return division

    async def update(self, division_id: int, update: DivisionUpdate) -> Division | None:
        division = await self.get(division_id)
        if division is None:
            return None
        data = update.model_dump()
        for field, value in data.items():
            setattr(division, field, value)
        await self.session.commit()
        await self.session.refresh(division)
        return division

    async def delete(self, division_id: int) -> None:
        division = await self.get(division_id)
        if division is None:
            return None
        await self.session.delete(division)
        await self.session.commit()
