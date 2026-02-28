from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.league import LeagueCreate, LeagueRead, LeagueUpdate
from src.models.team import TeamRead
from src.repositories.league import LeagueRepo
from src.services.league import LeagueService

league_router = APIRouter(prefix="/league", tags=["league"])


@league_router.get("", response_model=Sequence[LeagueRead])
async def list_leagues(
    limit: int | None = None,
    offset: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = LeagueRepo(session)
    return await repo.list(limit=limit, offset=offset)


@league_router.get("/{league_id}", response_model=LeagueRead)
async def get_league(
    league_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    league_service = LeagueService(session=session)
    return await league_service.get_league(league_id)


@league_router.get("/{league_id}/teams", response_model=Sequence[TeamRead])
async def get_league_teams(
    league_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    league_service = LeagueService(session=session)
    return await league_service.get_teams_for_league(league_id)


@league_router.post("", response_model=LeagueRead, status_code=status.HTTP_201_CREATED)
async def create_league(
    league_in: LeagueCreate,
    session: AsyncSession = Depends(get_async_session),
):
    league_service = LeagueService(session=session)
    return await league_service.create_league(league_in)


@league_router.put("/{league_id}", response_model=LeagueRead)
async def update_league(
    league_id: int,
    league_in: LeagueUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    repo = LeagueRepo(session)
    league = await repo.update(league_id, league_in)
    if league is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="League not found"
        )
    return league


@league_router.delete("/{league_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_league(
    league_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    repo = LeagueRepo(session)
    league = await repo.get(league_id)
    if league is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="League not found"
        )
    await repo.delete(league_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
