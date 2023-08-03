from typing import List

import sqlalchemy.exc
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import menu, submenu, dish
from database import get_async_session
from api.schemas import MenuRequest, MenuResponse, SubmenuRequest, SubmenuResponse, DishRequest, DishResponse
from sqlalchemy.sql.functions import count

router_menu = APIRouter(prefix='/api/v1/menus', tags=['Menu'])
router_submenu = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])
router_dish = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dish'])


@router_menu.get('/', response_model=List[MenuResponse])
async def get_all_menu(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)
    rows = await session.execute(query)
    rows = rows.fetchall()
    result = []
    for row in rows:
        query = select(submenu.c.id).where(submenu.c.menu_id == row.id)
        submenus = (await session.execute(query)).fetchall()
        dishes_count = 0
        for sb in submenus:
            query = select(dish).where(dish.c.submenu_id == sb[0])
            dishes_count += len((await session.execute(query)).fetchall())
        mr = MenuResponse(id=row.id, title=row.title, description=row.description, submenus_count=len(submenus), dishes_count=dishes_count)
        result.append(mr)
    return result


@router_menu.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.id == menu_id)
    row = await session.execute(query)
    row = row.fetchone()
    if row:    # if this id was found
        query = select(submenu.c.id).where(submenu.c.menu_id == row.id)
        submenus = (await session.execute(query)).fetchall()
        dishes_count = 0
        for sb in submenus:
            query = select(dish).where(dish.c.submenu_id == sb[0])
            dishes_count += len((await session.execute(query)).fetchall())
        mr = MenuResponse(id=row.id, title=row.title, description=row.description, submenus_count=len(submenus),
                          dishes_count=dishes_count)
        return mr
    else:
        raise HTTPException(status_code=404, detail="menu not found")


@router_menu.post('/', status_code=201, response_model=MenuResponse)
async def add_menu(new_menu: MenuRequest, session: AsyncSession = Depends(get_async_session)):
    query = insert(menu).values(**new_menu.model_dump()).returning('*')
    row = await session.execute(query)
    row = row.fetchone()
    mr = MenuResponse(id=row.id, title=row.title, description=row.description, submenus_count=0,
                      dishes_count=0)
    await session.commit()
    return mr


@router_menu.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, new_menu: MenuRequest, session: AsyncSession = Depends(get_async_session)):
    query = update(menu).where(menu.c.id == menu_id).values(**new_menu.model_dump()).returning('*')
    row = await session.execute(query)
    await session.commit()
    row = row.fetchone()
    if row:    # if this id was found
        query = select(submenu.c.id).where(submenu.c.menu_id == row.id)
        submenus = (await session.execute(query)).fetchall()
        dishes_count = 0
        for sb in submenus:
            query = select(dish).where(dish.c.submenu_id == sb[0])
            dishes_count += len((await session.execute(query)).fetchall())
        mr = MenuResponse(id=row.id, title=row.title, description=row.description, submenus_count=len(submenus),
                          dishes_count=dishes_count)
        return mr
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
    query = select(submenu, count(dish.c.id).label('dishes_count')).join(dish, dish.c.submenu_id == submenu.c.id, isouter=True).group_by(submenu.c.id)
    rows = await session.execute(query)
    rows = rows.fetchall()
    result = []
    for row in rows:
        sr = SubmenuResponse(**row._asdict())
        result.append(sr)
    return result


@router_submenu.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu, count(dish.c.id).label('dishes_count')).join(dish, dish.c.submenu_id == submenu.c.id, isouter=True).where(submenu.c.id == submenu_id).group_by(submenu.c.id)
    row = await session.execute(query)
    row = row.fetchone()
    if row:    # if this id was found
        return SubmenuResponse(**row._asdict())
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@router_submenu.post('/', status_code=201, response_model=SubmenuResponse)
async def add_submenu(menu_id: int, new_submenu: SubmenuRequest, session: AsyncSession = Depends(get_async_session)):
    new_submenu = new_submenu.model_dump()
    new_submenu['menu_id'] = menu_id  # adding fk field
    query = insert(submenu).values(**new_submenu).returning('*')
    try:
        row = await session.execute(query)
        row = row.fetchone()
        await session.commit()
        return SubmenuResponse(**row._asdict(), dishes_count=0)
    except sqlalchemy.exc.IntegrityError:  # ForeignKeyViolationError
        raise HTTPException(status_code=400, detail="menu not found")
    except Exception as e:
        print(e)


@router_submenu.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, new_submenu: MenuRequest, session: AsyncSession = Depends(get_async_session)):
    query = update(submenu).where(submenu.c.menu_id == menu_id).where(submenu.c.id == submenu_id).values(**new_submenu.model_dump()).returning('*')
    row = await session.execute(query)
    await session.commit()
    row = row.fetchone()
    if row:  # if this id was found
        # TODO: try to make it in one query
        query = select(dish).where(dish.c.submenu_id == submenu_id)
        dishes_count = len((await session.execute(query)).fetchall())
        return SubmenuResponse(**row._asdict(), dishes_count=dishes_count)
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
    rows = await session.execute(query)
    rows = rows.fetchall()
    result = []
    for row in rows:
        dr = DishResponse(**row._asdict())
        result.append(dr)
    return result


@router_dish.get('/{dish_id}', response_model=DishResponse)
async def get_dish(menu_id: int, submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(dish).where(dish.c.submenu_id == submenu_id).where(dish.c.id == dish_id)
    row = await session.execute(query)
    row = row.fetchone()
    if row:    # if this id was found
        return DishResponse(**row._asdict())
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@router_dish.post('/', status_code=201, response_model=DishResponse)
async def add_dish(menu_id: int, submenu_id: int, new_dish: DishRequest,
                      session: AsyncSession = Depends(get_async_session)):
    new_dish = new_dish.model_dump()
    # TODO: not valid rounding for 17.50 -> 17.5
    new_dish['price'] = str(round(float(new_dish['price']), 2))  # rounding price
    new_dish['submenu_id'] = submenu_id  # adding fk field
    query = insert(dish).values(**new_dish).returning('*')
    try:
        row = await session.execute(query)
        row = row.fetchone()
        await session.commit()
        return DishResponse(**row._asdict())
    except sqlalchemy.exc.IntegrityError:  # ForeignKeyViolationError
        raise HTTPException(status_code=400, detail="submenu not found")
    except Exception as e:
        print(e)


@router_dish.patch('/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, new_dish: DishRequest, session: AsyncSession = Depends(get_async_session)):
    new_dish = new_dish.model_dump()
    # TODO: not valid rounding for 17.50 -> 17.5
    new_dish['price'] = str(round(float(new_dish['price']), 2))  # rounding price
    query = update(dish).where(dish.c.id == dish_id).where(dish.c.submenu_id == submenu_id).values(**new_dish).returning('*')
    row = await session.execute(query)
    await session.commit()
    row = row.fetchone()
    if row:  # if this id was found
        return DishResponse(**row._asdict())
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@router_dish.delete('/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(dish).where(dish.c.id == dish_id).where(dish.c.submenu_id == submenu_id)
    await session.execute(query)
    await session.commit()
    return {}