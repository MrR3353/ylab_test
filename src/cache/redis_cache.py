import asyncio
import functools
from pickle import dumps, loads
from typing import Any

import redis.asyncio as redis

from config import CACHE_ENABLE, CACHE_EXPIRE_TIME, RUN_ON_DOCKER


def switch(func):  # for enable/disable cache methods
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if CACHE_ENABLE:
            return await func(*args, **kwargs)
        else:
            return asyncio.sleep(0)  # for await

    return wrapper


def cached(key: str):   # caching get responses, getting or setting key
    def inner(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache = await RedisCache().get(key)
            if cache is not None:
                return cache
            else:
                result = await func(*args, **kwargs)
                await RedisCache().set(key, result)
                return result
        return wrapper
    return inner


class RedisCache:
    def __init__(self):
        host = 'redis' if RUN_ON_DOCKER else 'localhost'  # docker/localhost hosts
        self.connect = redis.Redis(host=host, port=6379)

    @switch
    async def set(self, key: str, value: Any) -> None:
        value = dumps(value)
        await self.connect.set(name=key, value=value, ex=CACHE_EXPIRE_TIME)

    @switch
    async def get(self, key: str) -> Any:
        value = await self.connect.get(name=key)
        if value is not None:
            value = loads(value)
        return value

    @switch
    async def delete(self, key: str, is_pattern=False) -> None:
        await self.connect.delete(key)
        if is_pattern:
            async for key in self.connect.scan_iter(key + '*'):
                await self.connect.delete(key)

    @switch
    async def clear(self) -> None:
        await self.delete('', is_pattern=True)
