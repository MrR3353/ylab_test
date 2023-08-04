from typing import List

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, update, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import menu, submenu, dish
from database import get_async_session
from api.schemas import MenuRequest, MenuResponse, SubmenuRequest, SubmenuResponse, DishRequest, DishResponse
from sqlalchemy.sql.functions import count
from api.repositories.menu import MenuRepository
from api.repositories.submenu import SubmenuRepository
from api.repositories.dish import DishRepository


router_menu = APIRouter(prefix='/api/v1/menus', tags=['Menu'])
router_submenu = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])
router_dish = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dish'])

# mr = MenuRepository(Depends(get_async_session))


@router_menu.get('/', response_model=List[MenuResponse])
async def get_all_menu(mr: MenuRepository = Depends()):
    return await mr.get_all()


@router_menu.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, mr: MenuRepository = Depends()):
    return await mr.get(id=menu_id)


@router_menu.post('/', status_code=201, response_model=MenuResponse)
async def add_menu(data: MenuRequest, mr: MenuRepository = Depends()):
    return await mr.create(data)


@router_menu.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, data: MenuRequest, mr: MenuRepository = Depends()):
    return await mr.update(menu_id, data)


@router_menu.delete('/{menu_id}')
async def delete_menu(menu_id: int, mr: MenuRepository = Depends()):
    return await mr.delete(menu_id)


@router_menu.delete('/')
async def delete_all_menu(mr: MenuRepository = Depends()):
    return await mr.delete_all()


# TODO: maybe need to check menu_id for submenus???
@router_submenu.get('/', response_model=List[SubmenuResponse])
async def get_all_submenu(menu_id: int, sr: SubmenuRepository = Depends()):
    return await sr.get_all()


@router_submenu.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int, sr: SubmenuRepository = Depends()):
    return await sr.get(id=submenu_id)


@router_submenu.post('/', status_code=201, response_model=SubmenuResponse)
async def add_submenu(menu_id: int, data: SubmenuRequest, sr: SubmenuRepository = Depends()):
    return await sr.create(menu_id, data)


@router_submenu.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, data: SubmenuRequest, sr: SubmenuRepository = Depends()):
    return await sr.update(submenu_id, data)


@router_submenu.delete('/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int, sr: SubmenuRepository = Depends()):
    return await sr.delete(submenu_id)


# TODO: maybe need to check menu_id, submenu_id for dishes???
@router_dish.get('/', response_model=List[DishResponse])
async def get_all_dishes(menu_id: int, submenu_id: int, dr: DishRepository = Depends()):
    return await dr.get_all(submenu_id)


@router_dish.get('/{dish_id}', response_model=DishResponse)
async def get_dish(menu_id: int, submenu_id: int, dish_id: int, dr: DishRepository = Depends()):
    return await dr.get(id=dish_id)


@router_dish.post('/', status_code=201, response_model=DishResponse)
async def add_dish(menu_id: int, submenu_id: int, data: DishRequest, dr: DishRepository = Depends()):
    return await dr.create(submenu_id, data)


@router_dish.patch('/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, data: DishRequest, dr: DishRepository = Depends()):
    return await dr.update(dish_id, data)


@router_dish.delete('/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, dr: DishRepository = Depends()):
    return await dr.delete(dish_id)
