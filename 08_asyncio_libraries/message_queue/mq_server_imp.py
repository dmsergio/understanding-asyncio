import asyncio
from asyncio import StreamReader, StreamWriter, gather, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict

from msgproto import read_msg, send_msg


SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
SEND_QUEUES: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)
CHAN_QUEUES: Dict[bytes, Queue] = {}


async def client(reader: StreamReader, writer: StreamWriter):
    peer_name = writer.get_extra_info("peername")
    subscribe_channel = await read_msg(reader)
    SUBSCRIBERS[subscribe_channel].append(writer)
    send_task = asyncio.create_task(send_client(writer, SEND_QUEUES[writer]))
    print(f"Remote {peer_name} subscribed to {subscribe_channel}")
    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            if channel_name not in CHAN_QUEUES:
                CHAN_QUEUES[channel_name] = Queue(maxsize=10)
                asyncio.create_task(chan_sender(channel_name))
            await CHAN_QUEUES[channel_name].put(data)
    except asyncio.CancelledError:
        print(f"Remote {peer_name} closing connection")
    except asyncio.IncompleteReadError:
        print(f"Remote {peer_name} disconnected")
    finally:
        print(f"Remote {peer_name} closed")
        await SEND_QUEUES[writer].put(None)
        await send_task
        del SEND_QUEUES[writer]
        SUBSCRIBERS[subscribe_channel].remove(writer)


async def send_client(writer: StreamWriter, queue: Queue):
    while True:
        try:
            data = await queue.get()
        except asyncio.CancelledError:
            continue

        if not data:
            break

        try:
            await send_msg(writer, data)
        except asyncio.CancelledError:
            await send_msg(writer, data)

    writer.close()
    await writer.wait_closed()


async def chan_sender(name: bytes):
    with suppress(asyncio.CancelledError):
        while True:
            writers = SUBSCRIBERS[name]
            if not writers:
                await asyncio.sleep(1)
                continue
            if name.startswith(b"/queue"):
                writers.rotate()
                writers = [writers[0]]
            if not (msg := await CHAN_QUEUES[name].get()):
                break
            for writer in writers:
                if not SEND_QUEUES[writer].full():
                    print(f"Sending to {name}: {msg[:19]}...")
                    await SEND_QUEUES[writer].put(msg)


async def main(*args, **kwargs):
    server = await asyncio.start_server(client, host="127.0.0.1", port=25000)
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main(client, host="127.0.0.1", port=25000))
except KeyboardInterrupt:
    print("Bye!")
