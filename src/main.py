from fastapi import FastAPI

from api.redis_cache import RedisCache
from api.routers.dish import router_dish
from api.routers.menu import router_menu
from api.routers.submenu import router_submenu
from config import CACHE_ON

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)

if CACHE_ON:
    @app.on_event('startup')
    @app.on_event('shutdown')
    async def clear_cache():
        cache = RedisCache()
        await cache.clear()

# cd src && uvicorn main:app --reload
# pytest -v -s tests/
# redis in docker
