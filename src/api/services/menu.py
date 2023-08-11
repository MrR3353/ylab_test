from fastapi import Depends

from api.models import menu
from api.redis_cache import RedisCache, cached
from api.repositories.menu import MenuRepository
from api.schemas import MenuDetailsResponse, MenuRequest

'''
MENU:
get_all_menu  - cache(get_all_menu)
get_menu - cache(get_menu)
add_menu - cache(get_menu) + invalidation (get_all_menu)
update_menu - cache(get_menu) + invalidation (get_all_menu)
delete_menu - invalidation (get_all_menu, get_menu, SUBMENU, DISH)
'''


class MenuService:
    def __init__(self, db_repo: MenuRepository = Depends()):
        self.db_repo = db_repo
        self.cache = RedisCache()

    async def get_all(self) -> list[menu]:
        @cached(key='m:')
        async def wrapper():
            result = await self.db_repo.get_all()
            return result
        return await wrapper()

    async def get(self, **kwargs) -> menu:
        @cached(key=f"m:{kwargs['id']}:")
        async def wrapper():
            result = await self.db_repo.get(**kwargs)
            return result
        return await wrapper()

    async def create(self, data: MenuRequest) -> menu:
        result = await self.db_repo.create(data)
        await self.cache.delete('m:')
        await self.cache.set(f'm:{result.id}:', result)
        return result

    async def update(self, menu_id: int, data: MenuRequest) -> menu:
        result = await self.db_repo.update(menu_id, data)
        await self.cache.delete('m:')
        await self.cache.set(f'm:{menu_id}:', result)
        return result

    async def delete(self, menu_id: int) -> None:
        result = await self.db_repo.delete(menu_id)
        await self.cache.delete('m:')
        await self.cache.delete(f'm:{menu_id}:', is_pattern=True)  # cascade deleting
        return result

    async def delete_all(self) -> None:
        result = await self.db_repo.delete_all()
        await self.cache.delete('m:', is_pattern=True)  # cascade deleting
        return result

    async def get_all_with_submenu_dishes(self) -> list[MenuDetailsResponse]:
        result = await self.db_repo.get_all_with_submenu_dishes()
        return result
