from fastapi import APIRouter, BackgroundTasks, Depends

from api.schemas import MenuDetailsResponse, MenuRequest, MenuResponse
from api.services.menu import MenuService

router_menu = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router_menu.get('/', response_model=list[MenuResponse], summary='Возвращает список всех меню')
async def get_all(service: MenuService = Depends()):
    return await service.get_all()


@router_menu.get('/details', response_model=list[MenuDetailsResponse], summary='Возвращает список всех меню со всеми связанными подменю и блюдами')
async def get_all_with_submenu_dishes(service: MenuService = Depends()):
    return await service.get_all_with_submenu_dishes()


@router_menu.get('/{menu_id}', response_model=MenuResponse, summary='Возвращает меню по id')
async def get(menu_id: int, service: MenuService = Depends()):
    return await service.get(id=menu_id)


@router_menu.post('/', status_code=201, response_model=MenuResponse, summary='Добавляет новое меню')
async def create(data: MenuRequest, background_tasks: BackgroundTasks, service: MenuService = Depends()):
    return await service.create(data, background_tasks)


@router_menu.patch('/{menu_id}', response_model=MenuResponse, summary='Обновляет меню по id')
async def update(menu_id: int, data: MenuRequest, background_tasks: BackgroundTasks, service: MenuService = Depends()):
    return await service.update(menu_id, data, background_tasks)


@router_menu.delete('/{menu_id}', summary='Удаляет меню по id')
async def delete(menu_id: int, background_tasks: BackgroundTasks, service: MenuService = Depends()):
    return await service.delete(menu_id, background_tasks)


@router_menu.delete('/', summary='Удаляет все меню')
async def delete_all(background_tasks: BackgroundTasks, service: MenuService = Depends()):
    return await service.delete_all(background_tasks)
