from typing import List

from fastapi import Depends

from api.models import dish
from api.repositories.dish import DishRepository
from api.schemas import DishRequest


class DishService:
    def __init__(self, db_repo: DishRepository = Depends()):
        self.db_repo = db_repo

    async def get_all(self, submenu_id: int) -> List[dish]:
        result = await self.db_repo.get_all(submenu_id)
        return result

    async def get(self, **kwargs) -> dish:
        result = await self.db_repo.get(**kwargs)
        return result

    async def create(self, submenu_id: int, data: DishRequest) -> dish:
        result = await self.db_repo.create(submenu_id, data)
        return result

    async def update(self, dish_id: int, data: DishRequest) -> dish:
        result = await self.db_repo.update(dish_id, data)
        return result

    async def delete(self, dish_id: int) -> None:
        result = await self.db_repo.delete(dish_id)
        return result
