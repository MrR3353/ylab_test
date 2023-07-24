from typing import Optional

from pydantic import BaseModel


class MenuRequest(BaseModel):
    title: str
    description: str


class MenuResponse(MenuRequest):
    id: str


class SubmenuRequest(MenuRequest):
    pass


class SubmenuResponse(MenuResponse):
    pass


class DishRequest(MenuRequest):
    price: str


class DishResponse(DishRequest):
    id: str
