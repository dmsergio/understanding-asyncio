import asyncio


async def f():
    return 123


async def main():
    result = await f()
    return result


if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
