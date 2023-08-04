from typing import List
from fastapi import APIRouter, Depends
from api.schemas import MenuRequest, MenuResponse, SubmenuRequest, SubmenuResponse, DishRequest, DishResponse
from api.repositories.submenu import SubmenuRepository


router_submenu = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


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
