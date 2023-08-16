from typing import Union

from fastapi import BackgroundTasks, Depends

from api.models import dish
from api.repositories.dish import DishRepository
from api.schemas import DishDetailsResponse, DishRequest
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
            return await self.apply_discount(result)
        return await wrapper()

    async def get(self, **kwargs) -> dish:
        @cached(key=ce.dish, menu_id=kwargs['menu_id'], submenu_id=kwargs['submenu_id'], dish_id=kwargs['id'])
        async def wrapper():
            result = await self.db_repo.get(id=kwargs['id'])    # menu_id dont contains in dish
            return (await self.apply_discount(result))[0]
        return await wrapper()

    async def create(self, menu_id: int, submenu_id: int, data: DishRequest, background_tasks: BackgroundTasks) -> dish:
        result = await self.db_repo.create(submenu_id, data)
        background_tasks.add_task(self.cache.delete, ce.menu_list, ce.menu, ce.submenu_list, ce.submenu, ce.dish_list,
                                  menu_id=menu_id, submenu_id=submenu_id)
        background_tasks.add_task(self.cache.set, ce.dish, result, menu_id=menu_id, submenu_id=submenu_id,
                                  dish_id=result.id)
        return result

    async def update(self, menu_id: int, submenu_id: int, dish_id: int, data: DishRequest, background_tasks: BackgroundTasks) -> dish:
        result = await self.db_repo.update(dish_id, data)
        background_tasks.add_task(self.cache.delete, ce.dish_list, ce.dish,
                                  menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        background_tasks.add_task(self.cache.set, ce.dish, result, menu_id=menu_id,
                                  submenu_id=submenu_id, dish_id=submenu_id)
        return result   # mb need to apply discount here

    async def delete(self, menu_id: int, submenu_id: int, dish_id: int, background_tasks: BackgroundTasks) -> None:
        result = await self.db_repo.delete(dish_id)

        background_tasks.add_task(self.cache.delete, ce.menu_list, ce.menu, ce.submenu_list, ce.submenu, ce.dish_list, ce.dish,
                                  menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return result

    async def apply_discount(self, dishes: Union[dish, list[dish], list[DishDetailsResponse]]) -> list[dish]:  # type ignore
        '''
        Gets one or list of dishes, apply discount to each of them and returns
        '''
        with_discount = []
        if not isinstance(dishes, list):
            dishes = [dishes]
        if len(dishes) > 0:
            if isinstance(dishes[0], dict):   # for menu with details
                for d in dishes:
                    discount = await self.cache.get(ce.discount, dish_id=d['id'])
                    if discount is not None:
                        new_price = float(d['price']) / 100 * (100 - discount)
                        new_price = str(round(float(new_price), 2))  # rounding price
                        d = {**d, 'price': str(new_price)}    # replace old price
                    with_discount.append(d)
            else:   # for dish methods
                for d in dishes:
                    discount = await self.cache.get(ce.discount, dish_id=d.id)
                    if discount is not None:
                        new_price = float(d.price) / 100 * (100 - discount)
                        new_price = str(round(float(new_price), 2))  # rounding price
                        d = {**d._asdict(), 'price': str(new_price)}    # replace old price
                    with_discount.append(d)
        return with_discount
