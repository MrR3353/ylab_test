from typing import List

from fastapi import Depends

from api.models import submenu
from api.redis_cache import RedisCache
from api.repositories.submenu import SubmenuRepository
from api.schemas import SubmenuRequest


class SubmenuService:
    def __init__(self, db_repo: SubmenuRepository = Depends()):
        self.db_repo = db_repo
        self.cache = RedisCache()

    async def get_all(self, menu_id: int) -> List[submenu]:
        cache = await self.cache.get(f'menu{menu_id}submenu')
        if cache is not None:
            return cache
        else:
            result = await self.db_repo.get_all(menu_id)
            await self.cache.set(f'menu{menu_id}submenu', result)
            return result

    async def get(self, **kwargs) -> submenu:
        cache = await self.cache.get(f"menu{kwargs['menu_id']}submenu{kwargs['id']}")
        if cache is not None:
            return cache
        else:
            result = await self.db_repo.get(**kwargs)
            await self.cache.set(f"menu{kwargs['menu_id']}submenu{kwargs['id']}", result)
            return result

    async def create(self, menu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.create(menu_id, data)
        await self.cache.delete(f'menu')
        await self.cache.delete(f'menu{menu_id}')
        await self.cache.delete(f'menu{menu_id}submenu')
        await self.cache.set(f'menu{menu_id}submenu{result.id}', result)
        return result

    async def update(self, menu_id: int, submenu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.update(submenu_id, data)
        await self.cache.delete(f'menu{menu_id}submenu')
        await self.cache.set(f'menu{menu_id}submenu{submenu_id}', result)
        return result

    async def delete(self, menu_id: int, submenu_id: int) -> None:
        result = await self.db_repo.delete(submenu_id)
        await self.cache.delete(f'menu')
        await self.cache.delete(f'menu{menu_id}')
        await self.cache.delete(f'menu{menu_id}submenu')
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}', is_pattern=True)    # cascade deleting
        return result
