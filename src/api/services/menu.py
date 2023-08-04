from typing import List
from fastapi import Depends
from api.models import menu
from api.repositories.menu import MenuRepository
from api.schemas import MenuRequest


class MenuService:
    def __init__(self, db_repo: MenuRepository = Depends()):
        self.db_repo = db_repo

    async def get_all(self) -> List[menu]:
        result = await self.db_repo.get_all()
        return result

    async def get(self, **kwargs) -> menu:
        result = await self.db_repo.get(**kwargs)
        return result

    async def create(self, data: MenuRequest) -> menu:
        result = await self.db_repo.create(data)
        return result

    async def update(self, menu_id: int, data: MenuRequest) -> menu:
        result = await self.db_repo.update(menu_id, data)
        return result

    async def delete(self, menu_id: int) -> None:
        result = await self.db_repo.delete(menu_id)
        return result

    async def delete_all(self) -> None:
        result = await self.db_repo.delete_all()
        return result
