from typing import List

from fastapi import Depends

from api.models import submenu
from api.repositories.submenu import SubmenuRepository
from api.schemas import SubmenuRequest


class SubmenuService:
    def __init__(self, db_repo: SubmenuRepository = Depends()):
        self.db_repo = db_repo

    async def get_all(self) -> List[submenu]:
        result = await self.db_repo.get_all()
        return result

    async def get(self, **kwargs) -> submenu:
        result = await self.db_repo.get(**kwargs)
        return result

    async def create(self, menu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.create(menu_id, data)
        return result

    async def update(self, submenu_id: int, data: SubmenuRequest) -> submenu:
        result = await self.db_repo.update(submenu_id, data)
        return result

    async def delete(self, submenu_id: int) -> None:
        result = await self.db_repo.delete(submenu_id)
        return result
