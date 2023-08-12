from fastapi import APIRouter, BackgroundTasks, Depends

from api.schemas import DishRequest, DishResponse
from api.services.dish import DishService

router_dish = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dish'])


# TODO: maybe need to check menu_id, submenu_id for dishes???
@router_dish.get('/', response_model=list[DishResponse], summary='Возвращает список всех блюд данных подменю и меню')
async def get_all(menu_id: int, submenu_id: int, service: DishService = Depends()):
    return await service.get_all(menu_id, submenu_id)


@router_dish.get('/{dish_id}', response_model=DishResponse, summary='Возвращает блюдо по id')
async def get(menu_id: int, submenu_id: int, dish_id: int, service: DishService = Depends()):
    return await service.get(menu_id=menu_id, submenu_id=submenu_id, id=dish_id)


@router_dish.post('/', status_code=201, response_model=DishResponse, summary='Добавляет новое блюдо')
async def create(menu_id: int, submenu_id: int, data: DishRequest, background_tasks: BackgroundTasks, service: DishService = Depends()):
    return await service.create(menu_id, submenu_id, data, background_tasks)


@router_dish.patch('/{dish_id}', response_model=DishResponse, summary='Обновляет блюдо по id')
async def update(menu_id: int, submenu_id: int, dish_id: int, data: DishRequest, background_tasks: BackgroundTasks, service: DishService = Depends()):
    return await service.update(menu_id, submenu_id, dish_id, data, background_tasks)


@router_dish.delete('/{dish_id}', summary='Удаляет блюдо по id')
async def delete(menu_id: int, submenu_id: int, dish_id: int, background_tasks: BackgroundTasks, service: DishService = Depends()):
    return await service.delete(menu_id, submenu_id, dish_id, background_tasks)
