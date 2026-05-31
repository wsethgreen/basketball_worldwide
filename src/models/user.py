from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    display_name: str
    email: str | None = None
    hashed_password: str | None = None
    primary_platform: str | None = None
    last_login_platform: str | None = None
    user_device_id: str | None = None
    steam_id: str | None = None
    steam_username: str | None = None
    xbox_id: str | None = None
    xbox_gamertag: str | None = None
    psn_id: str | None = None
    psn_username: str | None = None
    epic_id: str | None = None
    epic_username: str | None = None
    nintendo_id: str | None = None
    nintendo_username: str | None = None
    preferred_locale: str | None = None
    is_active: bool = True
    last_login_at: datetime | None = None


class UserRead(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseUser):
    pass


class UserBootstrap(BaseModel):
    user_device_id: str
    display_name: str
    platform: str
    preferred_locale: str | None = None


class UserUpdate(BaseModel):
    display_name: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    primary_platform: str | None = None
    last_login_platform: str | None = None
    user_device_id: str | None = None
    steam_id: str | None = None
    steam_username: str | None = None
    xbox_id: str | None = None
    xbox_gamertag: str | None = None
    psn_id: str | None = None
    psn_username: str | None = None
    epic_id: str | None = None
    epic_username: str | None = None
    nintendo_id: str | None = None
    nintendo_username: str | None = None
    preferred_locale: str | None = None
    is_active: bool | None = None
    last_login_at: datetime | None = None
