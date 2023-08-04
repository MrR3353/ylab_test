from typing import List
from fastapi import APIRouter, Depends
from api.schemas import MenuRequest, MenuResponse, SubmenuRequest, SubmenuResponse, DishRequest, DishResponse
from api.repositories.menu import MenuRepository


router_menu = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


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
