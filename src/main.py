from fastapi import FastAPI
from api.router import router_menu, router_submenu, router_dish

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)