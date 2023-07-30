from typing import List

import sqlalchemy.exc
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import menu, submenu, dish
from database import get_async_session
from api.schemas import MenuRequest, MenuResponse, SubmenuRequest, SubmenuResponse, DishRequest, DishResponse

router_menu = APIRouter(prefix='/api/v1/menus', tags=['Menu'])
router_submenu = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])
router_dish = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dish'])


@router_menu.get('/', response_model=List[MenuResponse])
async def get_all_menu(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)
    results = await session.execute(query)
    json_results = []
    for result in results:
        json_result = dict(zip(('id', 'title', 'description'), tuple(map(str, result))))
        menu_id = result[0]
        query = select(submenu.c.id).where(submenu.c.menu_id == menu_id)
        submenus = (await session.execute(query)).fetchall()
        dishes_count = 0
        for sb in submenus:
            query = select(dish).where(dish.c.submenu_id == sb[0])
            dishes_count += len((await session.execute(query)).fetchall())
        json_result['submenus_count'] = len(submenus)
        json_result['dishes_count'] = dishes_count
        json_results.append(json_result)
    return json_results


@router_menu.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    result = result.fetchall()
    if len(result):    # if this id was found
        json_result = dict(zip(('id', 'title', 'description'), tuple(map(str, result[0]))))
        query = select(submenu.c.id).where(submenu.c.menu_id == menu_id)
        submenus = (await session.execute(query)).fetchall()
        dishes_count = 0
        for sb in submenus:
            query = select(dish).where(dish.c.submenu_id == sb[0])
            dishes_count += len((await session.execute(query)).fetchall())
        json_result['submenus_count'] = len(submenus)
        json_result['dishes_count'] = dishes_count
        return json_result
    else:
        raise HTTPException(status_code=404, detail="menu not found")


@router_menu.post('/', response_model=MenuResponse)
async def add_menu(new_menu: MenuRequest, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = insert(menu).values(**new_menu.model_dump()).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = list(result.fetchone())  # tuple to list
    result[0] = str(result[0])  # convert to str for tests
    result = dict(zip(('id', 'title', 'description'), result))
    result['submenus_count'] = 0
    result['dishes_count'] = 0
    response.status_code = 201
    return result


@router_menu.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, new_menu: MenuRequest, session: AsyncSession = Depends(get_async_session)):
    query = update(menu).where(menu.c.id == menu_id).values(**new_menu.model_dump()).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = result.fetchall()
    if len(result):  # if this id was found
        json_result = dict(zip(('id', 'title', 'description'), tuple(map(str, result[0]))))
        query = select(submenu.c.id).where(submenu.c.menu_id == menu_id)
        submenus = (await session.execute(query)).fetchall()
        dishes_count = 0
        for sb in submenus:
            query = select(dish).where(dish.c.submenu_id == sb[0])
            dishes_count += len((await session.execute(query)).fetchall())
        json_result['submenus_count'] = len(submenus)
        json_result['dishes_count'] = dishes_count
        return json_result
    else:
        raise HTTPException(status_code=404, detail="menu not found")


@router_menu.delete('/{menu_id}')
async def delete_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(menu).where(menu.c.id == menu_id)
    await session.execute(query)
    await session.commit()
    return {}


@router_menu.delete('/')
async def delete_all_menu(session: AsyncSession = Depends(get_async_session)):
    query = delete(menu)
    await session.execute(query)
    await session.commit()
    return {}


@router_submenu.get('/', response_model=List[SubmenuResponse])
async def get_all_submenu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_id == menu_id)
    submenus = await session.execute(query)
    json_results = []
    for sb in submenus:
        json_result = dict(zip(('id', 'title', 'description'), tuple(map(str, sb))))
        query = select(dish).where(dish.c.submenu_id == int(sb[0]))
        dishes_count = len((await session.execute(query)).fetchall())
        json_result['dishes_count'] = dishes_count
        json_results.append(json_result)
    return json_results


@router_submenu.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id)
    result = await session.execute(query)
    result = result.fetchall()
    if len(result):    # if this id was found
        result = dict(zip(('id', 'title', 'description'), tuple(map(str, result[0]))))
        query = select(dish).where(dish.c.submenu_id == submenu_id)
        dishes_count = len((await session.execute(query)).fetchall())
        result['dishes_count'] = dishes_count
        return result
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@router_submenu.post('/', response_model=SubmenuResponse)
async def add_submenu(menu_id: int, new_submenu: SubmenuRequest, response: Response, session: AsyncSession = Depends(get_async_session)):
    new_submenu = new_submenu.model_dump()
    new_submenu['menu_id'] = menu_id  # adding fk field
    query = insert(submenu).values(**new_submenu).returning('*')
    try:
        result = await session.execute(query)
        await session.commit()
        result = result.fetchall()
        result = dict(zip(('id', 'title', 'description'), tuple(map(str, result[0]))))
        result['dishes_count'] = 0
        response.status_code = 201
        return result
    except sqlalchemy.exc.IntegrityError:  # ForeignKeyViolationError
        raise HTTPException(status_code=400, detail="menu not found")
    except Exception as e:
        print(e)


@router_submenu.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, new_submenu: MenuRequest, response: Response, session: AsyncSession = Depends(get_async_session)):
    query = update(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id).values(**new_submenu.model_dump()).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = result.fetchall()
    if len(result):  # if this id was found
        result = dict(zip(('id', 'title', 'description'), tuple(map(str, result[0]))))
        query = select(dish).where(dish.c.submenu_id == submenu_id)
        dishes_count = len((await session.execute(query)).fetchall())
        result['dishes_count'] = dishes_count
        return result
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@router_submenu.delete('/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id)
    await session.execute(query)
    await session.commit()
    return {}


# TODO: maybe need to check menu_id for dishes???
@router_dish.get('/', response_model=List[DishResponse])
async def get_all_dishes(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(dish).where(dish.c.submenu_id == submenu_id)
    results = await session.execute(query)
    json_result = []
    for result in results:
        json_result.append(dict(zip(('id', 'title', 'description', 'price'), tuple(map(str, result)))))
    return json_result


@router_dish.get('/{dish_id}', response_model=DishResponse)
async def get_dish(menu_id: int, submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(dish).where(dish.c.submenu_id == submenu_id).where(dish.c.id == dish_id)
    result = await session.execute(query)
    result = result.fetchall()
    if len(result):    # if this id was found
        result = dict(zip(('id', 'title', 'description', 'price'), tuple(map(str, result[0]))))
        return result
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@router_dish.post('/', response_model=DishResponse)
async def add_dish(menu_id: int, submenu_id: int, new_dish: DishRequest, response: Response,
                      session: AsyncSession = Depends(get_async_session)):
    new_dish = new_dish.model_dump()
    new_dish['price'] = str(round(float(new_dish['price']), 2))  # rounding price
    new_dish['submenu_id'] = submenu_id  # adding fk field
    query = insert(dish).values(**new_dish).returning('*')
    try:
        result = await session.execute(query)
        await session.commit()
        result = result.fetchall()
        result = dict(zip(('id', 'title', 'description', 'price'), tuple(map(str, result[0]))))
        response.status_code = 201
        return result
    except sqlalchemy.exc.IntegrityError:  # ForeignKeyViolationError
        raise HTTPException(status_code=400, detail="submenu not found")
    except Exception as e:
        print(e)


@router_dish.patch('/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, new_dish: DishRequest, session: AsyncSession = Depends(get_async_session)):
    new_dish = new_dish.model_dump()
    new_dish['price'] = str(round(float(new_dish['price']), 2))  # rounding price
    query = update(dish).where(dish.c.id == dish_id).where(dish.c.submenu_id == submenu_id).values(**new_dish).returning('*')
    result = await session.execute(query)
    await session.commit()
    result = result.fetchall()
    if len(result):  # if this id was found
        result = dict(zip(('id', 'title', 'description', 'price'), tuple(map(str, result[0]))))
        return result
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@router_dish.delete('/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(dish).where(dish.c.id == dish_id).where(dish.c.submenu_id == submenu_id)
    await session.execute(query)
    await session.commit()
    return {}