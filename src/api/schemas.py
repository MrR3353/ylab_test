from typing import Optional

from pydantic import BaseModel


class MenuCreate(BaseModel):
    # id: Optional[int] = 1
    title: str
    description: str


class Menu(BaseModel):
    id: int
    title: str
    description: str
