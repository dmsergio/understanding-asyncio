import inspect


async def f():
    return 123


def main():
    print(f"For Python f() is a function -> {type(f)}")
    print(f"But exactly is a coroutine function -> {inspect.iscoroutinefunction(f)}")

    # The coroutine is get when the coroutine function is invoked
    coro = f()
    print(f"Result of invoked f() function -> {type(coro)}")

    # To get the result of the coroutine manually...
    try:
        coro.send(None)
    except StopIteration as e:
        print(f"Value returned from coroutine: {e.value}")
    # The precedent code is only for show how to work internally coroutines.
    # Is work of the event loop to doing this tasks.


if __name__ == "__main__":
    main()
