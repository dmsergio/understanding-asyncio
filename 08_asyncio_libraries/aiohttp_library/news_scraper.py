import pathlib
from asyncio import gather, create_task
from string import Template
from typing import Callable, List, Tuple

from aiohttp import web, ClientSession
from bs4 import BeautifulSoup


async def news(request):
    sites = [
        ("http://edition.cnn.com", cnn_articles),
        ("http://www.aljazeera.com", aljazeera_articles),
    ]
    tasks = [create_task(news_fetch(*site)) for site in sites]
    await gather(*tasks)

    items = {
        text: (
            f"<div class='box {kind}'>"
            f"<span>"
            f"<a href='{href}'>{text}</a>"
            f"</span>"
            f"</div>"
        )
        for task in tasks for href, text, kind, in task.result()
    }
    content = "".join(items[x] for x in sorted(items))

    file = open(str(pathlib.Path(__file__).parent.resolve()) + "/index.html")
    page = Template(file.read())
    return web.Response(
        body=page.safe_substitute(body=content),
        content_type="text/html",
    )


async def news_fetch(
    url: str,
    post_process: Callable,
) -> List[Tuple[str, str, str]]:
    proxy_url = (
        f"http://localhost:8050/render.html?"
        f"url={url}&timeout=60&wait=1"
    )
    async with ClientSession() as session:
        async with session.get(proxy_url) as resp:
            data = await resp.read()
            data = data.decode("utf-8")
    return post_process(url, data)


def cnn_articles(url: str, page_data: str) -> List[Tuple[str, str, str]]:
    return get_articles_by_provider(url, page_data, "cnn")


def aljazeera_articles(url: str, page_data: str) -> List[Tuple[str, str, str]]:
    return get_articles_by_provider(url, page_data, "aljazeera")


def get_articles_by_provider(
    url: str,
    page_data: str,
    provider: str,
) -> List[Tuple[str, str, str]]:
    soup = BeautifulSoup(page_data, "lxml")

    def cnn_match(tag):
        return (
            tag.text
            and tag.has_attr("href")
            and tag["href"].startswith("/")
            and tag["href"].endswith(".html")
            and tag.find(class_="cd__headline-text")
        )

    def aljazeera_match(tag):
        return (
            tag.text
            and tag.has_attr("href")
            and tag["href"].startswith("/news")
            and tag["href"].endswith(".html")
        )

    headlines = soup.find_all(locals()[f"{provider}_match"])
    return [
        (url + hl["href"], hl.text, provider)
        for hl in headlines
    ]


app = web.Application()
app.router.add_get("/news", news)
web.run_app(app, port=8080)
