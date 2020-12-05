import heapq

from ir.p3.data.posting import Posting


class PostingsList:
    def __init__(self, max_items):
        self._queue = []
        self._max_items = max_items

    def insert_posting(self, posting: Posting):
        if len(self._queue) < self._max_items:
            heapq.heappush(self._queue, (-posting.term_frequency, posting.doc_id, posting))
        elif -posting.term_frequency < self._queue[0][0]:
            heapq.heappop(self._queue)
            heapq.heappush(self._queue, (-posting.term_frequency, posting.doc_id, posting))

    def get_document_frequency(self):
        return len(self._queue)

    def get_postings(self):
        return [element[2] for element in heapq.nsmallest(self._max_items, self._queue)]

    def __iter__(self):
        yield from self.get_postings()
