from typing import List
from fastapi import Depends
from api.models import menu
from api.redis_cache import RedisCache
from api.repositories.menu import MenuRepository
from api.schemas import MenuRequest


class MenuService:
    def __init__(self, db_repo: MenuRepository = Depends()):
        self.db_repo = db_repo
        self.cache = RedisCache()

    async def get_all(self) -> List[menu]:
        cache = await self.cache.get('menu')
        if cache is not None:
            return cache
        else:
            result = await self.db_repo.get_all()
            await self.cache.set('menu', result)
            return result

    async def get(self, **kwargs) -> menu:
        cache = await self.cache.get(f"menu{kwargs['id']}")
        if cache is not None:
            return cache
        else:
            result = await self.db_repo.get(**kwargs)
            await self.cache.set(f"menu{kwargs['id']}", result)
            return result

    async def create(self, data: MenuRequest) -> menu:
        result = await self.db_repo.create(data)
        await self.cache.delete('menu')
        await self.cache.set(f'menu{result.id}', result)
        return result

    async def update(self, menu_id: int, data: MenuRequest) -> menu:
        result = await self.db_repo.update(menu_id, data)
        await self.cache.delete('menu')
        await self.cache.set(f"menu{menu_id}", result)
        return result

    async def delete(self, menu_id: int) -> None:
        result = await self.db_repo.delete(menu_id)
        await self.cache.delete('menu')
        await self.cache.delete(f'menu{menu_id}', is_pattern=True)  # cascade deleting
        return result

    async def delete_all(self) -> None:
        result = await self.db_repo.delete_all()
        await self.cache.delete('menu', is_pattern=True)  # cascade deleting
        return result
