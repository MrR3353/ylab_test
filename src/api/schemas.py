from decimal import Decimal
from typing import Optional
import sqlalchemy
from pydantic import BaseModel


class MenuRequest(BaseModel):
    title: str
    description: str


class MenuResponse(MenuRequest):
    id: str
    submenus_count: int
    dishes_count: int


class SubmenuRequest(MenuRequest):
    pass


class SubmenuResponse(SubmenuRequest):
    id: str
    dishes_count: int


class DishRequest(MenuRequest):
    price: str


class DishResponse(DishRequest):
    id: str
    price: str
