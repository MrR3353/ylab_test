from typing import List
from fastapi import APIRouter, Depends
from api.schemas import DishRequest, DishResponse
from api.services.dish import DishService

router_dish = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dish'])


# TODO: maybe need to check menu_id, submenu_id for dishes???
@router_dish.get('/', response_model=List[DishResponse])
async def get_all_dishes(menu_id: int, submenu_id: int, service: DishService = Depends()):
    return await service.get_all(submenu_id)


@router_dish.get('/{dish_id}', response_model=DishResponse)
async def get_dish(menu_id: int, submenu_id: int, dish_id: int, service: DishService = Depends()):
    return await service.get(id=dish_id)


@router_dish.post('/', status_code=201, response_model=DishResponse)
async def add_dish(menu_id: int, submenu_id: int, data: DishRequest, service: DishService = Depends()):
    return await service.create(submenu_id, data)


@router_dish.patch('/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, data: DishRequest, service: DishService = Depends()):
    return await service.update(dish_id, data)


@router_dish.delete('/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, service: DishService = Depends()):
    return await service.delete(dish_id)
