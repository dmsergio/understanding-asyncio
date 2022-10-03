import asyncio
from asyncio import StreamReader, StreamWriter, gather
from collections import deque, defaultdict
from typing import Deque, DefaultDict

from msgproto import read_msg, send_msg


SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)

async def client(reader: StreamReader, writer: StreamWriter):
    peer_name = writer.get_extra_info("peername")
    subscribe_channel = await read_msg(reader)
    SUBSCRIBERS[subscribe_channel].append(writer)
    print(f"Remote {peer_name} subscribed to {subscribe_channel}")
    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            print(f"Sending to {channel_name}: {data[:19]}...")
            conns = SUBSCRIBERS[channel_name]
            if conns and channel_name.startswith(b"/queue"):
                conns.rotate()
                conns = [conns[0]]
            await gather(*[send_msg(c, data) for c in conns])
    except asyncio.CancelledError:
        print(f"Remote {peer_name} closing connection")
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        print(f"Remote {peer_name} disconnected")
    finally:
        print(f"Remote {peer_name} closed")
        SUBSCRIBERS[subscribe_channel].remove(writer)


async def main(*args, **kwargs):
    server = await asyncio.start_server(client, host="127.0.0.1", port=25000)
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main(client, host="127.0.0.1", port=25000))
except KeyboardInterrupt:
    print("Bye!")
