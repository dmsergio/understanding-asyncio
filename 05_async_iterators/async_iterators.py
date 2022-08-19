class Iter:
    def __iter__(self):
        self.x = 0
        return self

    def __next__(self):
        if self.x > 2:
            raise StopIteration
        self.x += 1
        return self.x


class AsyncIter:
    def __aiter__(self):  # async def must not be set!
        self.x = 0
        return self

    async def __anext__(self):
        if self.x > 2:
            raise StopAsyncIteration
        self.x += 1
        return self.x
