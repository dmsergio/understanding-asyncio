
# Asyncio (understanding how it works)

Based on the book [Using asyncio in Python](https://www.oreilly.com/library/view/using-asyncio-in/9781492075325/).

Here is the official Python documentation for [asyncio](https://docs.python.org/3/library/asyncio.html).

### Subset of the main _API asyncio_ offers to end-user developers

1. Starting the __asyncio__ event loop.
2. Calling _async_/_await_ functions.
3. Creating a _task_ to be run on the loop.
4. Waiting for multiple tasks to complete.
5. Closing the loop after all concurrent tasks have completed.

### Features of asyncio arranged in a hierarchy
(The most important tiers for end-user developers are highlighted in bold)

| Level  | Concept                    | Implementation                                                                |
|--------|----------------------------|-------------------------------------------------------------------------------|
| Tier 9 | **Network: streams**       | StreamReader, StreamWritter, asyncio.open_connecion(), asyncio.start_server() |
| Tier 8 | Network: TCP & UPD         | Protocol                                                                      |
| Tier 7 | Network: transports        | BaseTransport                                                                 |
| Tier 6 | **Tools**                  | asyncio.Queue                                                                 |
| Tier 5 | **Subprocesses & threads** | run_in_executor(), asuncio.subprocess                                         |
| Tier 4 | Tasks                      | asyncio.Task, asyncio.create_task()                                           |
| Tier 3 | Futures                    | asyncio.Future                                                                |
| Tier 2 | **Event loop**             | asyncio.run(), BaseEventLoop                                                  |
| Tier 1 | **Coroutines**             | async def, async with, async for, await                                       |

#### Which I should focus it to use the *asyncio* library?
For an end-user developer, you should to learn the following tears:

- **Tier 1**: Is essential understanding how to write *async def* functions and use *await* to call and execute other corouteines.
- **Tier 2**: Start, shutdown, and interact with the event loop in essential.
- **Tier 5**: Executors are necessary to use blocking code in your *async* application.
- **Tier 6**: Use *asyncio.Queue* to distribute data between coroutines.
- **Tier 9**: The streams API gives you the simples way to handle socket communication over a network.

### Coroutines
A coroutine is an awaitable function that the result will be returned when the event loop has been obtained its result.

Example code:

```python
import asyncio

async def f():
    await asyncio.wait(0)
    return "coroutine finished!"

result = asyncio.run(f())
```

- **asyncio.run()** should be used as a main entry point for asyncio programs. The function does the followings steps:
  1. It ensures doesn't exist another event loop running in the same thread.
  2. Check has received a coroutine as a main argument.
  3. It creates a new event loop.
  4. It executes the coroutine and returns its value.
  5. It ensures to finish all the coroutines.
  6. It ensures to close the event loop.
