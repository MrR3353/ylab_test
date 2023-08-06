import functools

import redis.asyncio as redis
from pickle import dumps, loads
import asyncio

CACHE_ON = None


def switch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if CACHE_ON:
            return func(*args, **kwargs)
        else:
            return asyncio.sleep(0)  # for await
    return wrapper


class RedisCache:
    def __init__(self, cache_on=True):
        global CACHE_ON
        CACHE_ON = cache_on
        self.connect = redis.Redis()

    @switch
    async def set(self, key, value):
        value = dumps(value)
        await self.connect.set(name=key, value=value)

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


