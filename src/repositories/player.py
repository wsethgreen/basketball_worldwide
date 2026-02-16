from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.db.models.player import Player
from src.models.player import PlayerDto
from src.repositories.base import BaseRepo


class PlayerRepo(BaseRepo):
    async def get(self, player_id: str) -> Player | None:
        return await self.session.get(Player, player_id)

    async def get_players_for_team(self, team_id: int) -> Sequence[Player]:
        statement = (
            select(Player)
            .where(Player.team_id == team_id)
            .options(
                selectinload(Player.attributes),
                selectinload(Player.game_stats),
            )
        )
        result = await self.session.execute(statement)

        return result.scalars().all()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[Player]:
        stmt = select(Player).options(
            selectinload(Player.attributes),
            selectinload(Player.game_stats),
        )
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def create(self, player_dto: PlayerDto) -> Player:
        new_player = player_dto.model_dump(exclude={"attributes"})
        player = Player(**new_player)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)

        return player

    async def update(self, player_id: str, update: PlayerDto) -> Player | None:
        player = await self.get(player_id)
        if player is None:
            return None
        data = update.model_dump(exclude={"attributes"})
        for field, value in data.items():
            setattr(player, field, value)
        await self.session.commit()
        await self.session.refresh(player)

        return player

    async def delete(self, player_id: str) -> None:
        player = await self.get(player_id)
        if player is None:
            return None
        await self.session.delete(player)
        await self.session.commit()

    async def delete_players_from_team(self, team_id: int):
        statement = delete(Player).where(Player.team_id == team_id)
        result = await self.session.execute(statement)
        await self.session.commit()

        return result
