from decimal import Decimal
from typing import Optional, Union
import sqlalchemy
from pydantic import BaseModel, Field, AfterValidator, StrictStr, validator, field_validator
from typing_extensions import Annotated


class MenuRequest(BaseModel):
    title: str
    description: str


# TODO: use UUID or convert to str faster
IntToStr = Annotated[Union[int, str], AfterValidator(lambda num: str(num))]


class MenuResponse(MenuRequest):
    id: IntToStr
    submenus_count: int = 0
    dishes_count: int = 0


class SubmenuRequest(MenuRequest):
    pass


class SubmenuResponse(SubmenuRequest):
    id: IntToStr
    dishes_count: int = 0


def check_num(v: str) -> str:
    float(v)
    return v


StrContainingNum = Annotated[str, AfterValidator(check_num)]


class DishRequest(MenuRequest):
    price: StrContainingNum = Field(examples=['12.51'])


class DishResponse(DishRequest):
    id: IntToStr
    price: str
