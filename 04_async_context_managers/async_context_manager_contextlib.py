from contextlib import asynccontextmanager


async def download_webpage(url): ...


async def update_stats(url): ...


@asynccontextmanager
async def web_page(url):
    data = await download_webpage(url)
    yield data
    await update_stats(url)


async with web_page("google.com") as data: ...
