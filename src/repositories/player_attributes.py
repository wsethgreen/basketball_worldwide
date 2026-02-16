from typing import Sequence

from sqlalchemy import select

from src.db.models.player_attributes import PlayerAttributes
from src.models.player import PlayerAttributesDto
from src.repositories.base import BaseRepo


class PlayerAttributesRepo(BaseRepo):
    async def get(self, attributes_id: str) -> PlayerAttributes | None:
        return await self.session.get(PlayerAttributes, attributes_id)

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[PlayerAttributes]:
        stmt = select(PlayerAttributes)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def create(self, new_attributes: PlayerAttributesDto) -> PlayerAttributes:
        data = new_attributes.model_dump()
        attributes = PlayerAttributes(**data)
        self.session.add(attributes)
        await self.session.commit()
        await self.session.refresh(attributes)

        return attributes

    async def update(
        self, attributes_id: str, update: PlayerAttributesDto
    ) -> PlayerAttributes | None:
        attributes = await self.get(attributes_id)
        if attributes is None:
            return None
        data = update.model_dump()
        for field, value in data.items():
            setattr(attributes, field, value)
        await self.session.commit()
        await self.session.refresh(attributes)

        return attributes

    async def delete(self, attributes_id: str) -> None:
        attributes = await self.get(attributes_id)
        if attributes is None:
            return None
        await self.session.delete(attributes)
        await self.session.commit()
