import asyncio
import time


async def hello_world():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(2.0)
    print(f"{time.ctime()} Goodbye!")


def main():
    loop = asyncio.get_event_loop()
    task = loop.create_task(hello_world())
    loop.run_until_complete(task)
    pending = asyncio.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
    group = asyncio.gather(*pending, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()


if __name__ == "__main__":
    main()
