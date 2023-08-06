from fastapi import Depends

from api.models import dish
from api.redis_cache import RedisCache, cached
from api.repositories.dish import DishRepository
from api.schemas import DishRequest


class DishService:
    def __init__(self, db_repo: DishRepository = Depends()):
        self.db_repo = db_repo
        self.cache = RedisCache()

    async def get_all(self, menu_id: int, submenu_id: int) -> list[dish]:
        @cached(key=f'm:{menu_id}:s:{submenu_id}:d:')
        async def wrapper():
            result = await self.db_repo.get_all(submenu_id)
            return result
        return await wrapper()

    async def get(self, **kwargs) -> dish:
        @cached(key=f"m:{kwargs['menu_id']}:s:{kwargs['submenu_id']}:d:{kwargs['id']}:")
        async def wrapper():
            result = await self.db_repo.get(id=kwargs['id'])    # menu_id dont contains in dish
            return result
        return await wrapper()

    async def create(self, menu_id: int, submenu_id: int, data: DishRequest) -> dish:
        result = await self.db_repo.create(submenu_id, data)
        await self.cache.delete('m:')
        await self.cache.delete(f'm:{menu_id}:')
        await self.cache.delete(f'm:{menu_id}:s:')
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:')
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:d:')
        await self.cache.set(f'm:{menu_id}:s:{submenu_id}:d:{result.id}:', result)
        return result

    async def update(self, menu_id: int, submenu_id: int, dish_id: int, data: DishRequest) -> dish:
        result = await self.db_repo.update(dish_id, data)
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:d:')
        await self.cache.set(f'm:{menu_id}:s:{submenu_id}:d:{dish_id}:', result)
        return result

    async def delete(self, menu_id: int, submenu_id: int, dish_id: int) -> None:
        result = await self.db_repo.delete(dish_id)
        await self.cache.delete('m:')
        await self.cache.delete(f'm:{menu_id}:')
        await self.cache.delete(f'm:{menu_id}:s:')
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:')
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:d:')
        await self.cache.delete(f'm:{menu_id}:s:{submenu_id}:d:{dish_id}:', is_pattern=True)  # cascade deleting
        return result
