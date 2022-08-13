import asyncio


async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    f.set_result("I have finished.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    print(f"Is future done? {future.done()}")

    loop.create_task(main(future))
    loop.run_until_complete(future)
    print(f"Is future done? {future.done()}")
    print(f"Future result: {future.result()}")
