from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.user import UserBootstrap, UserCreate, UserRead, UserUpdate
from src.repositories.user import UserRepo
from src.services.user import UserService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("", response_model=Sequence[UserRead])
async def list_users(
    limit: int | None = None,
    offset: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    repo = UserRepo(session)
    return await repo.list(limit=limit, offset=offset)


@user_router.get("/platform/{platform}/{platform_id}", response_model=UserRead)
async def get_user_by_platform_id(
    platform: str,
    platform_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session=session)
    return await service.get_user_by_platform_id(platform, platform_id)


@user_router.post("/bootstrap", response_model=UserRead)
async def bootstrap_user(
    user_in: UserBootstrap,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session=session)
    return await service.bootstrap_user(user_in)


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session=session)
    return await service.get_user(user_id)


@user_router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session=session)
    return await service.create_user(user_in)


@user_router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session=session)
    return await service.update_user(user_id, user_in)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    service = UserService(session=session)
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
