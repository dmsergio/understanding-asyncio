import asyncio


async def doubler(n: int):
    for i in range(n):
        yield i, i * 2
        await asyncio.sleep(0.1)


async def main():
    # comprehension lists
    result = [x async for x in doubler(3)]
    print(f"Comprehension {type(result).__name__}", result, sep=" => ")

    # comprehension dicts
    result = {x: y async for x, y in doubler(3)}
    print(f"Comprehension {type(result).__name__}", result, sep=" => ")

    # comprehension sets
    result = {x async for x in doubler(3)}
    print(f"Comprehension {type(result).__name__}", result, sep=" => ")


if __name__ == "__main__":
    asyncio.run(main())
