import sqlalchemy
from fastapi import Depends, HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from api.models import dish, submenu
from api.schemas import SubmenuRequest, SubmenuResponse
from database import get_async_session


class SubmenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_all(self, menu_id: int) -> list[submenu]:
        query = select(submenu, count(dish.c.id).label('dishes_count'))\
            .join(dish, dish.c.submenu_id == submenu.c.id, isouter=True).group_by(submenu.c.id)\
            .where(submenu.c.menu_id == menu_id)
        rows = await self.session.execute(query)
        return rows.all()

    async def get(self, **kwargs) -> submenu:
        query = select(submenu, count(dish.c.id).label('dishes_count')).filter_by(**kwargs).\
            join(dish, dish.c.submenu_id == submenu.c.id, isouter=True).group_by(submenu.c.id)
        row = await self.session.execute(query)
        row = row.first()
        if not row:
            raise HTTPException(status_code=404, detail='submenu not found')
        return row

    async def create(self, menu_id: int, data: SubmenuRequest) -> submenu:
        new_submenu = data.model_dump()
        new_submenu['menu_id'] = menu_id  # adding fk field
        query = insert(submenu).values(**new_submenu).returning('*')
        try:
            row = await self.session.execute(query)
            await self.session.commit()
            return row.first()
        except sqlalchemy.exc.IntegrityError:  # ForeignKeyViolationError
            raise HTTPException(status_code=400, detail='menu not found')
        except Exception as e:
            print(e)

    async def update(self, submenu_id: int, data: SubmenuRequest) -> submenu:
        query = update(submenu).where(submenu.c.id == submenu_id). \
            values(**data.model_dump()).returning('*')
        row = await self.session.execute(query)
        await self.session.commit()
        row = row.first()
        if not row:
            raise HTTPException(status_code=404, detail='submenu not found')
        # TODO: try to make it in one query
        query = select(dish).where(dish.c.submenu_id == submenu_id)
        dishes_count = len((await self.session.execute(query)).all())
        return SubmenuResponse(**row._asdict(), dishes_count=dishes_count)

    async def delete(self, submenu_id: int) -> None:
        query = delete(submenu).where(submenu.c.id == submenu_id)
        await self.session.execute(query)
        await self.session.commit()
        return None
