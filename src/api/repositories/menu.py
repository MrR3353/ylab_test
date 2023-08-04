from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select, distinct, text, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count, func

from api.models import menu, submenu, dish
from database import get_async_session

from api.schemas import MenuRequest


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_all(self) -> List[menu]:
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
            raise HTTPException(status_code=404, detail="menu not found")
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
            raise HTTPException(status_code=404, detail="menu not found")
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
