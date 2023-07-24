from typing import Optional

from fastapi import FastAPI, Response
from pydantic import BaseModel
from api.router import router

app = FastAPI()

app.include_router(router)


# MENU = []
# LAST_ID = 0
#
#
# class Menu(BaseModel):
#     id: Optional[str] = "1"
#     title: str
#     description: str



# @app.get('/api/v1/menus')
# def get_menu():
#     return MENU
#
#
# @app.post('/api/v1/menus')
# def add_menu(new_menu: Menu, response: Response):
#     global LAST_ID
#     LAST_ID += 1
#     new_menu.id = str(LAST_ID)
#     MENU.append(new_menu)
#     print(MENU)
#     response.status_code = 201
#     return MENU[-1]