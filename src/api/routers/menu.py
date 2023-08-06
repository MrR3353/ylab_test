from fastapi import APIRouter, Depends

from api.schemas import MenuRequest, MenuResponse
from api.services.menu import MenuService

router_menu = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router_menu.get('/', response_model=list[MenuResponse])
async def get_all_menu(service: MenuService = Depends()):
    return await service.get_all()


@router_menu.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, service: MenuService = Depends()):
    return await service.get(id=menu_id)


@router_menu.post('/', status_code=201, response_model=MenuResponse)
async def add_menu(data: MenuRequest, service: MenuService = Depends()):
    return await service.create(data)


@router_menu.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, data: MenuRequest, service: MenuService = Depends()):
    return await service.update(menu_id, data)


@router_menu.delete('/{menu_id}')
async def delete_menu(menu_id: int, service: MenuService = Depends()):
    return await service.delete(menu_id)


@router_menu.delete('/')
async def delete_all_menu(service: MenuService = Depends()):
    return await service.delete_all()
