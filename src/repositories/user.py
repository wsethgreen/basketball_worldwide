from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from src.db.models.user import User
from src.models.user import UserCreate, UserUpdate
from src.repositories.base import BaseRepo


class UserRepo(BaseRepo):
    async def get(self, user_id: UUID | str) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user_device_id(self, user_device_id: str) -> User | None:
        statement = select(User).where(User.user_device_id == user_device_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_platform_id(self, platform: str, platform_id: str) -> User | None:
        platform_id_columns = {
            "steam": User.steam_id,
            "xbox": User.xbox_id,
            "psn": User.psn_id,
            "epic": User.epic_id,
            "nintendo": User.nintendo_id,
        }
        column = platform_id_columns.get(platform)
        if column is None:
            return None

        statement = select(User).where(column == platform_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[User]:
        stmt = select(User)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: UUID | str, update: UserUpdate) -> User | None:
        user = await self.get(user_id)
        if user is None:
            return None

        data = update.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID | str) -> None:
        user = await self.get(user_id)
        if user is None:
            return None
        await self.session.delete(user)
        await self.session.commit()
