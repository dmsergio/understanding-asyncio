import asyncio


async def f():
    await asyncio.sleep(0)
    return 123


def main():
    def run_getting_event_loop():
        loop = asyncio.get_event_loop()
        coro = f()
        result = loop.run_until_complete(coro)
        print(result)

    def run():
        result = asyncio.run(f())
        print(result)

    run_getting_event_loop()
    run()


if __name__ == "__main__":
    main()
