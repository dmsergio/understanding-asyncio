from time import ctime

from twisted.internet import asyncioreactor
# This is how you tell Twisted to use the asyncio event loop as its main
# reactor. This line must come before the reactor is imported from
# twisted.internet
asyncioreactor.install()
from twisted.internet import defer, reactor, task


async def main():
    for i in range(5):
        print(f"{ctime()} Hello {i}")
        await task.deferLater(reactor, 1, lambda: None)
        
        
defer.ensureDeferred(main())
reactor.run()
