from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from src.db.models.player_character import PlayerCharacter
from src.models.player_character import PlayerCharacterCreate, PlayerCharacterUpdate
from src.repositories.base import BaseRepo


class PlayerCharacterRepo(BaseRepo):
    async def get(self, player_character_id: UUID | str) -> PlayerCharacter | None:
        return await self.session.get(PlayerCharacter, player_character_id)

    async def get_by_team_id(self, team_id: int) -> PlayerCharacter | None:
        statement = select(PlayerCharacter).where(PlayerCharacter.team_id == team_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID | str) -> Sequence[PlayerCharacter]:
        statement = select(PlayerCharacter).where(PlayerCharacter.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[PlayerCharacter]:
        stmt = select(PlayerCharacter)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(
        self, player_character_in: PlayerCharacterCreate
    ) -> PlayerCharacter:
        player_character = PlayerCharacter(**player_character_in.model_dump())
        self.session.add(player_character)
        await self.session.commit()
        await self.session.refresh(player_character)
        return player_character

    async def update(
        self,
        player_character_id: UUID | str,
        update: PlayerCharacterUpdate,
    ) -> PlayerCharacter | None:
        player_character = await self.get(player_character_id)
        if player_character is None:
            return None

        data = update.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(player_character, field, value)
        await self.session.commit()
        await self.session.refresh(player_character)
        return player_character

    async def delete(self, player_character_id: UUID | str) -> None:
        player_character = await self.get(player_character_id)
        if player_character is None:
            return None
        await self.session.delete(player_character)
        await self.session.commit()
