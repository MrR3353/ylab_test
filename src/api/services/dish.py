from fastapi import BackgroundTasks, Depends

from api.models import dish
from api.repositories.dish import DishRepository
from api.schemas import DishRequest
from cache.cache_repository import CacheEntity as ce
from cache.cache_repository import CacheRepository, cached

'''
DISH:
get_all_dish - cache(get_all_dish)
get_dish - cache(get_dish)
add_dish - cache(get_dish) + invalidation(get_all_dish, MENU, SUBMENU)
update_dish - cache(get_dish) + invalidation(get_all_dish)
delete_dish - invalidation(get_all_dish, get_dish, MENU, SUBMENU)
'''


class DishService:
    def __init__(self, db_repo: DishRepository = Depends()):
        self.db_repo = db_repo
        self.cache = CacheRepository()

    async def get_all(self, menu_id: int, submenu_id: int) -> list[dish]:
        @cached(key=ce.dish_list, menu_id=menu_id, submenu_id=submenu_id)
        async def wrapper():
            result = await self.db_repo.get_all(submenu_id)
            return result
        return await wrapper()

    async def get(self, **kwargs) -> dish:
        @cached(key=ce.dish, menu_id=kwargs['menu_id'], submenu_id=kwargs['submenu_id'], dish_id=kwargs['id'])
        async def wrapper():
            result = await self.db_repo.get(id=kwargs['id'])    # menu_id dont contains in dish
            return result
        return await wrapper()

    async def create(self, menu_id: int, submenu_id: int, data: DishRequest, background_tasks: BackgroundTasks) -> dish:
        result = await self.db_repo.create(submenu_id, data)
        # await self.cache.delete(ce.menu_list, ce.menu, ce.submenu_list, ce.submenu, ce.dish_list,
        #                         menu_id=menu_id, submenu_id=submenu_id)
        # await self.cache.set(ce.dish, result, menu_id=menu_id, submenu_id=submenu_id, dish_id=result.id)
        background_tasks.add_task(self.cache.delete, ce.menu_list, ce.menu, ce.submenu_list, ce.submenu, ce.dish_list,
                                  menu_id=menu_id, submenu_id=submenu_id)
        background_tasks.add_task(self.cache.set, ce.dish, result, menu_id=menu_id, submenu_id=submenu_id,
                                  dish_id=result.id)
        return result

    async def update(self, menu_id: int, submenu_id: int, dish_id: int, data: DishRequest, background_tasks: BackgroundTasks) -> dish:
        result = await self.db_repo.update(dish_id, data)
        # await self.cache.delete(ce.dish_list, ce.dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        # await self.cache.set(ce.dish, result, menu_id=menu_id, submenu_id=submenu_id, dish_id=submenu_id)
        background_tasks.add_task(self.cache.delete, ce.dish_list, ce.dish,
                                  menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        background_tasks.add_task(self.cache.set, ce.dish, result, menu_id=menu_id,
                                  submenu_id=submenu_id, dish_id=submenu_id)
        return result

    async def delete(self, menu_id: int, submenu_id: int, dish_id: int, background_tasks: BackgroundTasks) -> None:
        result = await self.db_repo.delete(dish_id)
        # await self.cache.delete(ce.menu_list, ce.menu, ce.submenu_list, ce.submenu, ce.dish_list, ce.dish,
        #                         menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        background_tasks.add_task(self.cache.delete, ce.menu_list, ce.menu, ce.submenu_list, ce.submenu, ce.dish_list, ce.dish,
                                  menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return result
