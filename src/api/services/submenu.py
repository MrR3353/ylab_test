from typing import List

from fastapi import Depends

from api.models import submenu
from api.redis_cache import RedisCache, cached
from api.repositories.submenu import SubmenuRepository
from api.schemas import SubmenuRequest


class SubmenuService:
    def __init__(self, db_repo: SubmenuRepository = Depends()):
        self.db_repo = db_repo
        self.cache = RedisCache()

    async def get_all(self, menu_id: int) -> List[submenu]:
        @cached(key=f'm:{menu_id}:s:')
        async def wrapper():
            result = await self.db_repo.get_all(menu_id)
            return result
        return await wrapper()

    async def get(self, **kwargs) -> submenu:
        @cached(key=f"m:{kwargs['menu_id']}:s:{kwargs['id']}:")
        async def wrapper():
            result = await self.db_repo.get(**kwargs)
            return result
        return await wrapper()

    async def create(self, menu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.create(menu_id, data)
        await self.cache.delete('m:')
        await self.cache.delete(f'm:{menu_id}:')
        await self.cache.delete(f'm:{menu_id}:s:')
        await self.cache.set(f'm:{menu_id}:s:{result.id}:', result)
        return result

    async def update(self, menu_id: int, submenu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.update(submenu_id, data)
        await self.cache.delete(f'm:{menu_id}:s:')
        await self.cache.set(f'm:{menu_id}:s:{submenu_id}:', result)
        return result

    async def delete(self, menu_id: int, submenu_id: int) -> None:
        result = await self.db_repo.delete(submenu_id)
        await self.cache.delete('m:')
        await self.cache.delete(f'm:{menu_id}:')
        await self.cache.delete(f'm:{menu_id}:s:')
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:', is_pattern=True)    # cascade deleting
        return result
