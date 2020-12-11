import heapq
from typing import List, Tuple


class RankedDocumentsQueue:
    def __init__(self, max_items):
        self._queue: List[Tuple[float, str]] = []
        self._max_items: int = max_items

    def insert_posting(self, rank: float, doc_id: str):
        if len(self._queue) < self._max_items:
            heapq.heappush(self._queue, (rank, doc_id))
        elif rank > self._queue[0][0]:
            heapq.heappop(self._queue)
            heapq.heappush(self._queue, (rank, doc_id))

    def get_document_frequency(self):
        return len(self._queue)

    def get_ranked_posting(self) -> List[Tuple[float, str]]:
        return [(element[0], element[1]) for element in heapq.nlargest(self._max_items, self._queue)]

    def __iter__(self) -> Tuple[float, str]:
        yield from self.get_ranked_posting()
