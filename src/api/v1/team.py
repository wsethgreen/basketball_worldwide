from __future__ import annotations

import random

from faker import Faker
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.team import TeamCreate, TeamRead, TeamUpdate
from src.repostories.team_repo import TeamRepo

team_router = APIRouter(prefix="/team", tags=["team"])


@team_router.get("", response_model=Sequence[TeamRead])
async def list_teams(
    limit: int | None = None,
    offset: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = TeamRepo(session)
    return await repo.list(limit=limit, offset=offset)


@team_router.get("/{team_id}", response_model=TeamRead)
async def get_team(
    team_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    repo = TeamRepo(session)
    team = await repo.get(team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@team_router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    session: AsyncSession = Depends(get_async_session),
):
    faker = Faker()
    # Needs improved badly
    NICKNAMES = [
        "Lions",
        "Wolves",
        "Eagles",
        "Hawks",
        "Bulls",
        "Tigers",
        "Falcons",
        "Sharks",
        "Raptors",
        "Panthers",
        "Kings",
        "Storm",
    ]

    # TODO: Add TeamService to handle business logic
    new_team = TeamCreate(
        league_id=team_in.league_id,
        city=faker.city(),
        nickname=random.choice(NICKNAMES),
        budget=random.randint(50, 125) * 1_000_000,
    )

    repo = TeamRepo(session)
    return await repo.create(new_team)


@team_router.put("/{team_id}", response_model=TeamRead)
async def update_team(
    team_id: int,
    team_in: TeamUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    repo = TeamRepo(session)
    team = await repo.update(team_id, team_in)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@team_router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    repo = TeamRepo(session)
    team = await repo.get(team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    await repo.delete(team_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
