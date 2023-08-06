from fastapi import FastAPI

from api.redis_cache import RedisCache
from api.routers.menu import router_menu
from api.routers.submenu import router_submenu
from api.routers.dish import router_dish

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)


@app.on_event('startup')
@app.on_event('shutdown')
async def clear_cache():
    cache = RedisCache()
    await cache.clear()

# cd src && uvicorn main:app --reload
# pytest -v -s tests/
