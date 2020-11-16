import heapq
from ir.p3.data.posting import Posting


class RankedDocumentQueue:
    def __init__(self):
        self._data = []
        self._index = 0
        heapq.heapify(self._data)

    def push(self, posting: Posting, rank: float):
        heapq.heappush(self._data, (rank, self._index, posting))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._data)[2]

    def __iter__(self):
        yield from reversed([element[2] for element in self._data])
