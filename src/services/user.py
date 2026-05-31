from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserBootstrap, UserCreate, UserUpdate
from src.repositories.user import UserRepo


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepo(session=session)

    async def create_user(self, user_in: UserCreate):
        await self._validate_unique_user_fields(user_in)
        return await self.user_repo.create(user_in)

    async def get_user(self, user_id: UUID):
        user = await self.user_repo.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def get_user_by_platform_id(self, platform: str, platform_id: str):
        normalized_platform = platform.lower()
        self._validate_platform(normalized_platform)

        user = await self.user_repo.get_by_platform_id(
            normalized_platform,
            platform_id,
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def bootstrap_user(self, user_in: UserBootstrap):
        now = datetime.now(timezone.utc)
        user = await self.user_repo.get_by_user_device_id(user_in.user_device_id)

        if user is not None:
            return await self.user_repo.update(
                user.id,
                UserUpdate(
                    last_login_at=now,
                    last_login_platform=user_in.platform,
                    preferred_locale=user_in.preferred_locale,
                ),
            )

        return await self.create_user(
            UserCreate(
                display_name=user_in.display_name,
                user_device_id=user_in.user_device_id,
                primary_platform=user_in.platform,
                last_login_platform=user_in.platform,
                preferred_locale=user_in.preferred_locale,
                last_login_at=now,
            )
        )

    async def update_user(self, user_id: UUID, user_in: UserUpdate):
        current = await self.get_user(user_id)
        await self._validate_unique_user_fields(
            user_in,
            current_user_id=current.id,
        )

        return await self.user_repo.update(user_id, user_in)

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.user_repo.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        await self.user_repo.delete(user_id)

    async def _validate_unique_user_fields(
        self,
        user_in: UserCreate | UserUpdate,
        current_user_id: UUID | None = None,
    ) -> None:
        data = user_in.model_dump(exclude_unset=True)

        email = data.get("email")
        if email is not None:
            existing_user = await self.user_repo.get_by_email(email)
            if existing_user is not None and existing_user.id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already assigned to another user",
                )

        user_device_id = data.get("user_device_id")
        if user_device_id is not None:
            existing_user = await self.user_repo.get_by_user_device_id(user_device_id)
            if existing_user is not None and existing_user.id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="user_device_id is already assigned to another user",
                )

        for platform in ("steam", "xbox", "psn", "epic", "nintendo"):
            field_name = f"{platform}_id"
            platform_id = data.get(field_name)
            if platform_id is None:
                continue

            existing_user = await self.user_repo.get_by_platform_id(
                platform,
                platform_id,
            )
            if existing_user is not None and existing_user.id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"{field_name} is already assigned to another user",
                )

    def _validate_platform(self, platform: str) -> None:
        valid_platforms = {"steam", "xbox", "psn", "epic", "nintendo"}
        if platform not in valid_platforms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Platform must be one of: {', '.join(sorted(valid_platforms))}",
            )
