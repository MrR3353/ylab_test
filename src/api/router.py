import json

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import menu, submenu
from database import get_async_session
from api.schemas import MenuCreate, SubmenuCreate
from asyncpg import exceptions

router = APIRouter(prefix='/api/v1', tags=['Api'])


@router.get('/menus')
async def get_all_menu(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)
    results = await session.execute(query)
    json_result = []
    for result in results:
        json_result.append(dict(zip(('id', 'title', 'description'), result)))
    return json_result


@router.get('/menus/{menu_id}')
async def get_menu(menu_id: int, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    result = result.fetchall()
    if len(result):    # if this id was found
        result = list(result[0])  # tuple to list
        result[0] = str(result[0])  # convert to str for tests
        result = dict(zip(('id', 'title', 'description'), result))
        return result
    else:
        response.status_code = 404
        return {'detail': 'menu not found'}


@router.post('/menus')
async def add_menu(new_menu: MenuCreate, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = insert(menu).values(**new_menu.dict()).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = list(result.fetchone())  # tuple to list
    result[0] = str(result[0])  # convert to str for tests
    result = dict(zip(('id', 'title', 'description'), result))
    response.status_code = 201
    return result


@router.patch('/menus/{menu_id}')
async def update_menu(menu_id: int, new_menu: MenuCreate, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = update(menu).where(menu.c.id == menu_id).values(**new_menu.dict()).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = result.fetchall()
    if len(result):  # if this id was found
        result = list(result[0])  # tuple to list
        result[0] = str(result[0])  # convert to str for tests
        result = dict(zip(('id', 'title', 'description'), result))
        return result
    else:
        response.status_code = 404
        return {'detail': 'menu not found'}


@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(menu).where(menu.c.id == menu_id)
    await session.execute(query)
    await session.commit()
    return {}


@router.delete('/menus')
async def delete_all_menu(session: AsyncSession = Depends(get_async_session)):
    query = delete(menu)
    await session.execute(query)
    await session.commit()
    return {}


@router.get('/menus/{menu_id}/submenus')
async def get_all_submenu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_id == menu_id)
    results = await session.execute(query)
    print(results)
    json_result = []
    for result in results:
        json_result.append(dict(zip(('id', 'title', 'description'), result)))
    return json_result


@router.get('/menus/{menu_id}/submenus/{submenu_id}')
async def get_submenu(menu_id: int, submenu_id: int, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id)
    result = await session.execute(query)
    result = result.fetchall()
    if len(result):    # if this id was found
        result = list(result[0])  # tuple to list
        result[0] = str(result[0])  # convert to str for tests
        result = dict(zip(('id', 'title', 'description'), result))
        return result
    else:
        response.status_code = 404
        return {'detail': 'submenu not found'}


@router.post('/menus/{menu_id}/submenus')
async def add_submenu(menu_id: int, new_submenu: SubmenuCreate, response: Response, session: AsyncSession = Depends(get_async_session)):
    new_submenu = new_submenu.dict()
    new_submenu['menu_id'] = menu_id  # adding fk field
    query = insert(submenu).values(**new_submenu).returning('*')
    try:
        result = await session.execute(query)
        await session.commit()
        result = list(result.fetchone())  # tuple to list
        result[0] = str(result[0])  # convert to str for tests
        result = dict(zip(('id', 'title', 'description'), result))
        response.status_code = 201
        return result
    except exceptions.ForeignKeyViolationError:
        #     cant catch this
        pass
    except Exception as e:
        if e.code == 'gkpj':
            return {'detail': 'menu not found'}
        else:
            print(e)



@router.patch('/menus/{menu_id}/submenus/{submenu_id}')
async def update_submenu(menu_id: int, submenu_id: int, new_submenu: MenuCreate, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = update(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id).values(**new_submenu.dict()).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = result.fetchall()
    if len(result):  # if this id was found
        result = list(result[0])  # tuple to list
        result[0] = str(result[0])  # convert to str for tests
        result = dict(zip(('id', 'title', 'description'), result))
        return result
    else:
        response.status_code = 404
        return {'detail': 'submenu not found'}


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id)
    await session.execute(query)
    await session.commit()
    return {}


@router.delete('/clear')
async def clear_all_tables(session: AsyncSession = Depends(get_async_session)):
    query = delete(menu)
    await session.execute(query)
    await session.commit()
    return {}