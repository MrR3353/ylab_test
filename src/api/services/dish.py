from typing import List

from fastapi import Depends

from api.models import dish
from api.redis_cache import RedisCache
from api.repositories.dish import DishRepository
from api.schemas import DishRequest


class DishService:
    def __init__(self, db_repo: DishRepository = Depends()):
        self.db_repo = db_repo
        self.cache = RedisCache()

    async def get_all(self, menu_id: int, submenu_id: int) -> List[dish]:
        cache = await self.cache.get(f'menu{menu_id}submenu{submenu_id}dish')
        if cache is not None:
            return cache
        else:
            result = await self.db_repo.get_all(submenu_id)
            await self.cache.set(f'menu{menu_id}submenu{submenu_id}dish', result)
            return result

    async def get(self, **kwargs) -> dish:
        cache = await self.cache.get(f"menu{kwargs['menu_id']}submenu{kwargs['submenu_id']}dish{kwargs['id']}")
        if cache is not None:
            return cache
        else:
            result = await self.db_repo.get(id=kwargs['id'])    # menu_id dont contains in dish
            await self.cache.set(f"menu{kwargs['menu_id']}submenu{kwargs['submenu_id']}dish{kwargs['id']}", result)
            return result

    async def create(self, menu_id: int, submenu_id: int, data: DishRequest) -> dish:
        result = await self.db_repo.create(submenu_id, data)
        await self.cache.delete(f'menu')
        await self.cache.delete(f'menu{menu_id}')
        await self.cache.delete(f'menu{menu_id}submenu')
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}')
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}dish')
        await self.cache.set(f'menu{menu_id}submenu{submenu_id}dish{result.id}', result)
        return result

    async def update(self, menu_id: int, submenu_id: int, dish_id: int, data: DishRequest) -> dish:
        result = await self.db_repo.update(dish_id, data)
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}dish')
        await self.cache.set(f'menu{menu_id}submenu{submenu_id}dish{dish_id}', result)
        return result

    async def delete(self, menu_id: int, submenu_id: int, dish_id: int) -> None:
        result = await self.db_repo.delete(dish_id)
        await self.cache.delete(f'menu')
        await self.cache.delete(f'menu{menu_id}')
        await self.cache.delete(f'menu{menu_id}submenu')
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}')
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}dish')
        await self.cache.delete(f'menu{menu_id}submenu{submenu_id}dish{dish_id}', is_pattern=True)  # cascade deleting
        return result
