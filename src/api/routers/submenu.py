from fastapi import APIRouter, BackgroundTasks, Depends

from api.schemas import SubmenuRequest, SubmenuResponse
from api.services.submenu import SubmenuService

router_submenu = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


# TODO: maybe need to check menu_id for submenus???
@router_submenu.get('/', response_model=list[SubmenuResponse], summary='Возвращает список всех подменю данного меню')
async def get_all(menu_id: int, service: SubmenuService = Depends()):
    return await service.get_all(menu_id)


@router_submenu.get('/{submenu_id}', response_model=SubmenuResponse, summary='Возвращает подменю по id')
async def get(menu_id: int, submenu_id: int, service: SubmenuService = Depends()):
    return await service.get(menu_id=menu_id, id=submenu_id)


@router_submenu.post('/', status_code=201, response_model=SubmenuResponse, summary='Добавляет новое подменю')
async def create(menu_id: int, data: SubmenuRequest, background_tasks: BackgroundTasks, service: SubmenuService = Depends()):
    return await service.create(menu_id, data, background_tasks)


@router_submenu.patch('/{submenu_id}', response_model=SubmenuResponse, summary='Обновляет подменю по id')
async def update(menu_id: int, submenu_id: int, data: SubmenuRequest, background_tasks: BackgroundTasks, service: SubmenuService = Depends()):
    return await service.update(menu_id, submenu_id, data, background_tasks)


@router_submenu.delete('/{submenu_id}', summary='Удаляет подменю по id')
async def delete(menu_id: int, submenu_id: int, background_tasks: BackgroundTasks, service: SubmenuService = Depends()):
    return await service.delete(menu_id, submenu_id, background_tasks)
