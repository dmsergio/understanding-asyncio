import asyncio
import time


async def hello_world():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(2.0)
    print(f"{time.ctime()} Goodbye!")


def main():
    asyncio.run(hello_world())


if __name__ == "__main__":
    main()
