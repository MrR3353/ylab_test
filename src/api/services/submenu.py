from fastapi import Depends

from api.cache_repository import CacheEntity as ce
from api.cache_repository import CacheRepository, cached
from api.models import submenu
from api.repositories.submenu import SubmenuRepository
from api.schemas import SubmenuRequest

'''
SUBMENU:
get_all_submenu  - cache(get_all_submenu)
get_submenu - cache(get_submenu)
add_submenu - cache(get_submenu) + invalidation (get_all_submenu, MENU, get_all_submenu)
update_submenu - cache(get_submenu) + invalidation (get_all_submenu)
delete_submenu - invalidation (get_all_submenu, get_submenu, MENU, DISH)
'''


class SubmenuService:
    def __init__(self, db_repo: SubmenuRepository = Depends()):
        self.db_repo = db_repo
        self.cache = CacheRepository()

    async def get_all(self, menu_id: int) -> list[submenu]:
        @cached(key=ce.submenu_list, menu_id=menu_id)
        async def wrapper():
            result = await self.db_repo.get_all(menu_id)
            return result
        return await wrapper()

    async def get(self, **kwargs) -> submenu:
        @cached(key=ce.submenu, menu_id=kwargs['menu_id'], submenu_id=kwargs['id'])
        async def wrapper():
            result = await self.db_repo.get(**kwargs)
            return result
        return await wrapper()

    async def create(self, menu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.create(menu_id, data)
        await self.cache.delete(ce.menu_list, ce.menu, ce.submenu_list, menu_id=menu_id)
        await self.cache.set(ce.submenu, result, menu_id=menu_id, submenu_id=result.id)
        return result

    async def update(self, menu_id: int, submenu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.update(submenu_id, data)
        await self.cache.delete(ce.submenu_list, ce.submenu, menu_id=menu_id, submenu_id=submenu_id)
        await self.cache.set(ce.submenu, result, menu_id=menu_id, submenu_id=result.id)
        return result

    async def delete(self, menu_id: int, submenu_id: int) -> None:
        result = await self.db_repo.delete(submenu_id)
        await self.cache.delete(ce.menu_list, ce.menu, ce.submenu_list, ce.submenu_cascade,
                                menu_id=menu_id, submenu_id=submenu_id)
        return result
