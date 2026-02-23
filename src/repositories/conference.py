from typing import Sequence

from sqlalchemy import select

from src.db.models.conference import Conference
from src.models.conference import ConferenceCreate, ConferenceUpdate
from src.repositories.base import BaseRepo


class ConferenceRepo(BaseRepo):
    async def get(self, conference_id: int) -> Conference | None:
        return await self.session.get(Conference, conference_id)

    async def get_conferences_for_league(self, league_id: int) -> Sequence[Conference]:
        statement = select(Conference).where(Conference.league_id == league_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[Conference]:
        stmt = select(Conference)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_conference: ConferenceCreate) -> Conference:
        data = new_conference.model_dump()
        conference = Conference(**data)
        self.session.add(conference)
        await self.session.commit()
        await self.session.refresh(conference)
        return conference

    async def update(
        self, conference_id: int, update: ConferenceUpdate
    ) -> Conference | None:
        conference = await self.get(conference_id)
        if conference is None:
            return None
        data = update.model_dump()
        for field, value in data.items():
            setattr(conference, field, value)
        await self.session.commit()
        await self.session.refresh(conference)
        return conference

    async def delete(self, conference_id: int) -> None:
        conference = await self.get(conference_id)
        if conference is None:
            return None
        await self.session.delete(conference)
        await self.session.commit()
