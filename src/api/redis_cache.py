import functools

import redis.asyncio as redis
from pickle import dumps, loads
import asyncio

CACHE_ON = None
EXPIRE_TIME = 60*60


def switch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if CACHE_ON:
            return func(*args, **kwargs)
        else:
            return asyncio.sleep(0)  # for await
    return wrapper


def cached(key: str):
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
    def __init__(self, cache_on=True):
        global CACHE_ON
        CACHE_ON = cache_on
        self.connect = redis.Redis()

    @switch
    async def set(self, key, value):
        value = dumps(value)
        await self.connect.set(name=key, value=value, ex=EXPIRE_TIME)

    @switch
    async def get(self, key):
        value = await self.connect.get(name=key)
        if value is not None:
            value = loads(value)
        return value

    @switch
    async def delete(self, key, is_pattern=False):
        await self.connect.delete(key)
        if is_pattern:
            async for key in self.connect.scan_iter(key + '*'):
                await self.connect.delete(key)

    @switch
    async def clear(self):
        await self.delete('', is_pattern=True)

