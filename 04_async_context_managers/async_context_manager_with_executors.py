"""
This example is to show how to implement asynchronous context managers
with blocking functions, because not always is possible to adapt the code
to convert blocking functions in coroutines (async def ...).
"""
import asyncio
from contextlib import asynccontextmanager


def download_webpage(url):
    # no coroutine function
    pass


def update_stats(url):
    # no coroutine function
    pass


@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, download_webpage, url)
    yield data
    await loop.run_in_executor(None, update_stats, url)


async with web_page("google.com") as data: ...
