import asyncio

import aioredis


async def main():
    redis = await aioredis.from_url(url="redis://localhost", port=6379)
    keys = ["Americas", "Africa", "Europe", "Asia"]

    async for value in OneAtTime(redis, keys):
        ...
        # await do_something_with(value)


class OneAtTime:
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys

    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    async def __anext__(self):
        try:
            k = next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration

        value = await self.redis.get(k)
        return value


asyncio.run(main())
