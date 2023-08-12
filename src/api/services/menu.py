from fastapi import Depends

from api.cache_repository import CacheEntity as ce
from api.cache_repository import CacheRepository, cached
from api.models import menu
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
        self.cache = CacheRepository()

    async def get_all(self) -> list[menu]:
        @cached(key=ce.menu_list)
        async def wrapper():
            result = await self.db_repo.get_all()
            return result
        return await wrapper()

    async def get(self, **kwargs) -> menu:
        @cached(key=ce.menu, menu_id=kwargs['id'])
        async def wrapper():
            result = await self.db_repo.get(**kwargs)
            return result
        return await wrapper()

    async def create(self, data: MenuRequest) -> menu:
        result = await self.db_repo.create(data)
        await self.cache.delete(ce.menu_list)
        await self.cache.set(ce.menu, result, menu_id=result.id)
        return result

    async def update(self, menu_id: int, data: MenuRequest) -> menu:
        result = await self.db_repo.update(menu_id, data)
        await self.cache.delete(ce.menu_list, ce.menu, menu_id=menu_id)
        await self.cache.set(ce.menu, result, menu_id=menu_id)
        return result

    async def delete(self, menu_id: int) -> None:
        result = await self.db_repo.delete(menu_id)
        await self.cache.delete(ce.menu_list, ce.menu_cascade, menu_id=menu_id)
        return result

    async def delete_all(self) -> None:
        result = await self.db_repo.delete_all()
        await self.cache.delete(ce.all)
        return result

    async def get_all_with_submenu_dishes(self) -> list[MenuDetailsResponse]:
        result = await self.db_repo.get_all_with_submenu_dishes()
        return result
