import asyncio
from contextlib import suppress


async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    try:
        f.set_result("I have finished.")
    except RuntimeError as e:
        print(f"No longer allowed: {e}")
        f.cancel()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.Task(asyncio.sleep(1_000_000))
    print(f"Is future done? {future.done()}")

    loop.create_task(main(future))

    with suppress(asyncio.CancelledError):
        loop.run_until_complete(future)

    print(f"Is future done? {future.done()}")
    print(f"Is future cancelled?: {future.cancelled()}")
