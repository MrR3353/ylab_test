from fastapi import FastAPI
from api.routers.menu import router_menu
from api.routers.submenu import router_submenu
from api.routers.dish import router_dish

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)