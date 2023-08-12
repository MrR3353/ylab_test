from fastapi import FastAPI

from api.routers.dish import router_dish
from api.routers.menu import router_menu
from api.routers.submenu import router_submenu
from cache.redis_cache import RedisCache
from config import CACHE_ENABLE

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)

if CACHE_ENABLE:
    @app.on_event('startup')
    async def clear_cache():
        cache = RedisCache()
        await cache.clear()

# Для запуска без Docker:
# В config.py установить RUN_ON_DOCKER = False
# Запустить сервер redis перед запуском
# В папке проекта:
# cd src && uvicorn main:app --reload
# pytest -v -s tests/
