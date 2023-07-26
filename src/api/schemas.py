from decimal import Decimal
from typing import Optional
import sqlalchemy
from pydantic import BaseModel, Field, AfterValidator
from typing_extensions import Annotated


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


def check_num(v: str) -> str:
    float(v)
    # assert v**0.5 % 1 == 0, f'{v} is not a square number'
    return v


StrContainingNum = Annotated[str, AfterValidator(check_num)]


class DishRequest(MenuRequest):
    price: StrContainingNum = Field(examples=['12.51'])


class DishResponse(DishRequest):
    id: str
    price: str
