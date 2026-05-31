from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.player_character import PlayerCharacterCreate, PlayerCharacterUpdate
from src.repositories.player_character import PlayerCharacterRepo
from src.repositories.team import TeamRepo


class PlayerCharacterService:
    def __init__(self, session: AsyncSession):
        self.player_character_repo = PlayerCharacterRepo(session=session)
        self.team_repo = TeamRepo(session=session)

    async def create_player_character(self, player_character_in: PlayerCharacterCreate):
        if player_character_in.team_id is not None:
            await self._validate_team_assignment(team_id=player_character_in.team_id)

        return await self.player_character_repo.create(player_character_in)

    async def get_player_character(self, player_character_id: UUID):
        player_character = await self.player_character_repo.get(player_character_id)
        if player_character is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player character not found",
            )
        return player_character

    async def get_player_character_for_team(self, team_id: int):
        player_character = await self.player_character_repo.get_by_team_id(team_id)
        if player_character is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player character not found for team",
            )
        return player_character

    async def update_player_character(
        self,
        player_character_id: UUID,
        player_character_in: PlayerCharacterUpdate,
    ):
        current = await self.get_player_character(player_character_id)

        if "team_id" in player_character_in.model_fields_set:
            team_id = player_character_in.team_id
            if team_id is not None:
                await self._validate_team_assignment(
                    team_id=team_id,
                    current_player_character_id=current.id,
                )

        return await self.player_character_repo.update(
            player_character_id,
            player_character_in,
        )

    async def delete_player_character(self, player_character_id: UUID) -> None:
        player_character = await self.player_character_repo.get(player_character_id)
        if player_character is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player character not found",
            )
        await self.player_character_repo.delete(player_character_id)

    async def _validate_team_assignment(
        self,
        team_id: int,
        current_player_character_id: UUID | None = None,
    ) -> None:
        team = await self.team_repo.get(team_id)
        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with id {team_id} not found",
            )

        assigned_character = await self.player_character_repo.get_by_team_id(team_id)
        if (
            assigned_character is not None
            and assigned_character.id != current_player_character_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Team with id {team_id} already has a player character",
            )
