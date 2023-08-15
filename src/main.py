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

# Запуск без Docker:
# Запустить сервер redis перед запуском
# В папке проекта:
# cd src && uvicorn main:app --reload
# Запуск тестов (запускать перед celery или в момент, когда celery ничего не выполняет):
# pytest -v -s tests/

# Запуск celery:
# cd src
# celery -A tasks.update_admin:celery worker --loglevel=INFO --pool=solo
# celery -A tasks.update_admin:celery beat --loglevel=INFO

# Запуск в Docker:
# Приложение + БД:
# `docker compose up --build`
#
# Тесты (запускать после приложения с БД):
# `docker compose -f docker-compose-test.yml up --build`
