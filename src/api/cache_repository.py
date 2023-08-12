import functools
from enum import Enum

from api.redis_cache import RedisCache, switch


class CacheEntity(Enum):
    menu_list = 'm:'
    menu = 'm:{menu_id}:'
    menu_cascade = 'm:{menu_id}:*'
    submenu_list = 'm:{menu_id}:s:'
    submenu = 'm:{menu_id}:s:{submenu_id}:'
    submenu_cascade = 'm:{menu_id}:s:{submenu_id}:*'
    dish_list = 'm:{menu_id}:s:{submenu_id}:d:'
    dish = 'm:{menu_id}:s:{submenu_id}:d:{dish_id}:'
    all = 'm:*'


# caching get responses, getting or setting key
def cached(key: CacheEntity, menu_id: int | None = None, submenu_id: int | None = None, dish_id: int | None = None):
    def inner(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache = await CacheRepository().get(key, menu_id, submenu_id, dish_id)
            if cache is not None:
                return cache
            else:
                result = await func(*args, **kwargs)
                await CacheRepository().set(key, result, menu_id, submenu_id, dish_id)
                return result
        return wrapper
    return inner


class CacheRepository:
    def __init__(self):
        self.redis = RedisCache()

    @switch
    async def get(self, key: CacheEntity, menu_id: int | None = None, submenu_id: int | None = None, dish_id: int | None = None):
        if key == CacheEntity.menu_list:
            return await self.redis.get('m:')
        else:
            assert menu_id is not None
            if key == CacheEntity.menu:
                return await self.redis.get(f'm:{menu_id}:')
            elif key == CacheEntity.submenu_list:
                return await self.redis.get(f'm:{menu_id}:s:')
            else:
                assert submenu_id is not None
                if key == CacheEntity.submenu:
                    return await self.redis.get(f'm:{menu_id}:s:{submenu_id}:')
                elif key == CacheEntity.dish_list:
                    return await self.redis.get(f'm:{menu_id}:s:{submenu_id}:d:')
                elif key == CacheEntity.dish:
                    assert dish_id is not None
                    return await self.redis.get(f'm:{menu_id}:s:{submenu_id}:d:{dish_id}:')

    @switch
    async def set(self, key: CacheEntity, value, menu_id: int | None = None, submenu_id: int | None = None, dish_id: int | None = None):
        if key == CacheEntity.menu_list:
            await self.redis.set('m:', value)
        else:
            assert menu_id is not None
            if key == CacheEntity.menu:
                await self.redis.set(f'm:{menu_id}:', value)
            elif key == CacheEntity.submenu_list:
                return await self.redis.set(f'm:{menu_id}:s:', value)
            else:
                assert submenu_id is not None
                if key == CacheEntity.submenu:
                    await self.redis.set(f'm:{menu_id}:s:{submenu_id}:', value)
                elif key == CacheEntity.dish_list:
                    return await self.redis.set(f'm:{menu_id}:s:{submenu_id}:d:', value)
                elif key == CacheEntity.dish:
                    assert dish_id is not None
                    await self.redis.set(f'm:{menu_id}:s:{submenu_id}:d:{dish_id}:', value)

    @switch
    async def delete(self, *args: CacheEntity, menu_id: int | None = None, submenu_id: int | None = None, dish_id: int | None = None):
        for arg in args:
            if arg == CacheEntity.menu_list:
                await self.redis.delete('m:')
            elif arg == CacheEntity.all:
                await self.redis.delete('m:', is_pattern=True)
            else:
                assert menu_id is not None
                if arg == CacheEntity.menu:
                    await self.redis.delete(f'm:{menu_id}:')
                elif arg == CacheEntity.menu_cascade:
                    await self.redis.delete(f'm:{menu_id}:', is_pattern=True)
                elif arg == CacheEntity.submenu_list:
                    await self.redis.delete(f'm:{menu_id}:s:')
                else:
                    assert submenu_id is not None
                    if arg == CacheEntity.submenu:
                        await self.redis.delete(f'm:{menu_id}:s:{submenu_id}:')
                    elif arg == CacheEntity.dish_list:
                        await self.redis.delete(f'm:{menu_id}:s:{submenu_id}:d:')
                    elif arg == CacheEntity.submenu_cascade:
                        await self.redis.delete(f'm:{menu_id}:s:{submenu_id}:', is_pattern=True)
                    else:
                        assert dish_id is not None
                        if arg == CacheEntity.dish:
                            await self.redis.delete(f'm:{menu_id}:s:{submenu_id}:d:{dish_id}:')
