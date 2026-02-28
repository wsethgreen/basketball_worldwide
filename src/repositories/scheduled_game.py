from typing import Sequence

from sqlalchemy import delete, select

from src.db.models.conference import Conference
from src.db.models.division import Division

from src.db.models.scheduled_game import ScheduledGame
from src.db.models.team import Team
from src.models.scheduled_game import ScheduledGameCreate, ScheduledGameUpdate
from src.repositories.base import BaseRepo


class ScheduledGameRepo(BaseRepo):
    async def get(self, game_id: int) -> ScheduledGame | None:
        return await self.session.get(ScheduledGame, game_id)

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[ScheduledGame]:
        stmt = select(ScheduledGame)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_for_team(
        self, team_id: int, season_year: int | None = None
    ) -> Sequence[ScheduledGame]:
        stmt = select(ScheduledGame).where(
            (ScheduledGame.home_team_id == team_id)
            | (ScheduledGame.away_team_id == team_id)
        )
        if season_year is not None:
            stmt = stmt.where(ScheduledGame.season_year == season_year)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, new_game: ScheduledGameCreate) -> ScheduledGame:
        data = new_game.model_dump()
        game = ScheduledGame(**data)
        self.session.add(game)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def create_many(
        self, new_games: Sequence[ScheduledGameCreate]
    ) -> Sequence[ScheduledGame]:
        if not new_games:
            return []
        records = [ScheduledGame(**game.model_dump()) for game in new_games]
        self.session.add_all(records)
        await self.session.commit()
        return records

    async def update(
        self, game_id: int, update: ScheduledGameUpdate
    ) -> ScheduledGame | None:
        game = await self.get(game_id)
        if game is None:
            return None
        data = update.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(game, field, value)
        await self.session.commit()
        await self.session.refresh(game)
        return game

    async def delete(self, game_id: int) -> None:
        game = await self.get(game_id)
        if game is None:
            return None
        await self.session.delete(game)
        await self.session.commit()

    async def delete_for_league_season(self, league_id: int, season_year: int) -> int:
        stmt = (
            delete(ScheduledGame)
            .where(ScheduledGame.season_year == season_year)
            .where(
                ScheduledGame.home_team_id.in_(
                    select(Team.id)
                    .join(Division, Team.division_id == Division.id)
                    .join(Conference, Division.conference_id == Conference.id)
                    .where(Conference.league_id == league_id)
                )
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount or 0
