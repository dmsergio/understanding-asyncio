import asyncio


async def f():
    try:
        while True: await asyncio.sleep(0)
    except asyncio.CancelledError:
        print("I was cancelled!")
    else:
        return 123


def main():
    coro = f()
    coro.send(None)
    coro.send(None)
    coro.throw(asyncio.CancelledError)


if __name__ == "__main__":
    main()
