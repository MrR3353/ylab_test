from typing import List

import sqlalchemy
from fastapi import Depends, HTTPException
from sqlalchemy import select, distinct, text, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count, func

from api.models import menu, submenu, dish
from database import get_async_session

from api.schemas import DishRequest


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_all(self, submenu_id: int) -> List[dish]:
        query = select(dish).where(dish.c.submenu_id == submenu_id)
        rows = await self.session.execute(query)
        return rows.all()

    async def get(self, **kwargs) -> dish:
        query = select(dish).filter_by(**kwargs)
        row = await self.session.execute(query)
        row = row.first()
        if not row:
            raise HTTPException(status_code=404, detail="dish not found")
        return row

    async def create(self, submenu_id: int, data: DishRequest) -> dish:
        new_dish = data.model_dump()
        # TODO: not valid rounding for 17.50 -> 17.5
        new_dish['price'] = str(round(float(new_dish['price']), 2))  # rounding price
        new_dish['submenu_id'] = submenu_id  # adding fk field
        query = insert(dish).values(**new_dish).returning('*')
        try:
            row = await self.session.execute(query)
            await self.session.commit()
            return row.first()
        except sqlalchemy.exc.IntegrityError:  # ForeignKeyViolationError
            raise HTTPException(status_code=400, detail="submenu not found")
        except Exception as e:
            print(e)

    async def update(self, dish_id: int, data: DishRequest) -> dish:
        new_dish = data.model_dump()
        # TODO: not valid rounding for 17.50 -> 17.5
        new_dish['price'] = str(round(float(new_dish['price']), 2))  # rounding price
        query = update(dish).where(dish.c.id == dish_id).values(**new_dish).returning('*')
        row = await self.session.execute(query)
        await self.session.commit()
        row = row.first()
        if not row:
            raise HTTPException(status_code=404, detail="dish not found")
        return row

    async def delete(self, dish_id: int) -> None:
        query = delete(dish).where(dish.c.id == dish_id)
        await self.session.execute(query)
        await self.session.commit()
        return None
