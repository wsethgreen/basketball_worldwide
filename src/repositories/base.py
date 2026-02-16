from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def get(self, obj_id: int | str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Sequence[Any]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, obj_in: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_id: Any, obj_in: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_id: Any) -> None:
        raise NotImplementedError
