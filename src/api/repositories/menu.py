from fastapi import Depends, HTTPException
from sqlalchemy import delete, distinct, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from api.models import dish, menu, submenu
from api.schemas import MenuDetailsResponse, MenuRequest
from database import get_async_session


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_all(self) -> list[menu]:
        query = select(menu, count(distinct(submenu.c.id)).label('submenus_count'),
                       count(dish.c.id).label('dishes_count'))\
            .join(submenu, submenu.c.menu_id == menu.c.id, isouter=True)\
            .join(dish, dish.c.submenu_id == submenu.c.id, isouter=True).group_by(menu.c.id)
        rows = await self.session.execute(query)
        rows = rows.all()
        return rows

    async def get(self, **kwargs) -> menu:
        query = select(menu, count(distinct(submenu.c.id)).label('submenus_count'),
                       count(dish.c.id).label('dishes_count')) \
            .filter_by(**kwargs)\
            .join(submenu, submenu.c.menu_id == menu.c.id, isouter=True)\
            .join(dish, dish.c.submenu_id == submenu.c.id, isouter=True)\
            .group_by(menu.c.id)
        row = await self.session.execute(query)
        row = row.first()
        if not row:
            raise HTTPException(status_code=404, detail='menu not found')
        return row

    async def create(self, data: MenuRequest) -> menu:
        query = insert(menu).values(**data.model_dump()).returning('*')
        row = await self.session.execute(query)
        await self.session.commit()
        return row.first()

    async def update(self, menu_id: int, data: MenuRequest) -> menu:
        query = update(menu).where(menu.c.id == menu_id).values(**data.model_dump()).returning('*')
        row = await self.session.execute(query)
        await self.session.commit()
        row = row.first()
        if not row:
            raise HTTPException(status_code=404, detail='menu not found')
        # TODO: try to make it in one query
        query = select(menu, count(distinct(submenu.c.id)).label('submenus_count'),
                       count(dish.c.id).label('dishes_count'))\
            .join(submenu, submenu.c.menu_id == menu.c.id, isouter=True)\
            .join(dish, dish.c.submenu_id == submenu.c.id, isouter=True).where(menu.c.id == menu_id).group_by(menu.c.id)
        row = await self.session.execute(query)
        return row.first()

    async def delete(self, menu_id: int) -> None:
        query = delete(menu).where(menu.c.id == menu_id)
        await self.session.execute(query)
        await self.session.commit()
        return None

    async def delete_all(self) -> None:
        query = delete(menu)
        await self.session.execute(query)
        await self.session.commit()
        return None

    async def get_all_with_submenu_dishes(self) -> list[MenuDetailsResponse]:
        query = select(menu, submenu.c.id.label('submenu_id'),
                       submenu.c.title.label('submenu_title'), submenu.c.description.label('submenu_description'),
                       dish.c.id.label('dish_id'), dish.c.title.label('dish_title'),
                       dish.c.description.label('dish_description'), dish.c.price.label('dish_price'),)\
            .join(submenu, submenu.c.menu_id == menu.c.id, isouter=True)\
            .join(dish, dish.c.submenu_id == submenu.c.id, isouter=True)
        rows = await self.session.execute(query)
        rows = rows.all()

        menus = []
        for row in rows:    # creating menus from rows
            new_menu = {'id': row.id, 'title': row.title, 'description': row.description, 'submenus': []}
            if new_menu not in menus:
                menus.append(new_menu)
        for row in rows:    # creating submenus from rows
            new_submenu = {'id': row.submenu_id, 'title': row.submenu_title,
                           'description': row.submenu_description, 'dishes': []}
            if new_submenu['id'] is not None:
                submenu_menu = list(filter(lambda some_menu: some_menu['id'] == row.id, menus))[
                    0]  # find menu for submenu
                if new_submenu not in submenu_menu['submenus']:
                    submenu_menu['submenus'].append(new_submenu)
        for row in rows:  # creating dishes from rows
            new_dish = {'id': row.dish_id, 'title': row.dish_title,
                        'description': row.dish_description, 'price': row.dish_price}
            if new_dish['id'] is not None:
                dish_menu = list(filter(lambda some_menu: some_menu['id'] == row.id, menus))[0]  # find menu for dish
                dish_submenu = list(filter(lambda some_submenu: some_submenu['id'] == row.submenu_id, dish_menu['submenus']))[
                    0]  # find submenu for dish
                dish_submenu['dishes'].append(new_dish)
        return menus
