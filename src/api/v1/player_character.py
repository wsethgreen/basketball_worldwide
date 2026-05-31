from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.player_character import (
    PlayerCharacterCreate,
    PlayerCharacterRead,
    PlayerCharacterUpdate,
)
from src.repositories.player_character import PlayerCharacterRepo
from src.services.player_character import PlayerCharacterService

player_character_router = APIRouter(
    prefix="/player-characters",
    tags=["player-characters"],
)


@player_character_router.get("", response_model=Sequence[PlayerCharacterRead])
async def list_player_characters(
    limit: int | None = None,
    offset: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = PlayerCharacterRepo(session)
    return await repo.list(limit=limit, offset=offset)


@player_character_router.get("/team/{team_id}", response_model=PlayerCharacterRead)
async def get_player_character_for_team(
    team_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    service = PlayerCharacterService(session=session)
    return await service.get_player_character_for_team(team_id)


@player_character_router.get(
    "/{player_character_id}", response_model=PlayerCharacterRead
)
async def get_player_character(
    player_character_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    service = PlayerCharacterService(session=session)
    return await service.get_player_character(player_character_id)


@player_character_router.post(
    "",
    response_model=PlayerCharacterRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_player_character(
    player_character_in: PlayerCharacterCreate,
    session: AsyncSession = Depends(get_async_session),
):
    service = PlayerCharacterService(session=session)
    return await service.create_player_character(player_character_in)


@player_character_router.put(
    "/{player_character_id}", response_model=PlayerCharacterRead
)
async def update_player_character(
    player_character_id: UUID,
    player_character_in: PlayerCharacterUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    service = PlayerCharacterService(session=session)
    return await service.update_player_character(
        player_character_id,
        player_character_in,
    )


@player_character_router.delete(
    "/{player_character_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_player_character(
    player_character_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    service = PlayerCharacterService(session=session)
    await service.delete_player_character(player_character_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
