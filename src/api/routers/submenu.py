from fastapi import APIRouter, Depends

from api.schemas import SubmenuRequest, SubmenuResponse
from api.services.submenu import SubmenuService

router_submenu = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


# TODO: maybe need to check menu_id for submenus???
@router_submenu.get('/', response_model=list[SubmenuResponse])
async def get_all_submenu(menu_id: int, service: SubmenuService = Depends()):
    return await service.get_all(menu_id)


@router_submenu.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int, service: SubmenuService = Depends()):
    return await service.get(menu_id=menu_id, id=submenu_id)


@router_submenu.post('/', status_code=201, response_model=SubmenuResponse)
async def add_submenu(menu_id: int, data: SubmenuRequest, service: SubmenuService = Depends()):
    return await service.create(menu_id, data)


@router_submenu.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, data: SubmenuRequest, service: SubmenuService = Depends()):
    return await service.update(menu_id, submenu_id, data)


@router_submenu.delete('/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int, service: SubmenuService = Depends()):
    return await service.delete(menu_id, submenu_id)
