def insert_posting(self, posting: Posting) -> None:
	if len(self._queue) < self._max_items:
		heapq.heappush(self._queue, (-posting.term_frequency, posting.doc_id, posting))
	elif -posting.term_frequency < self._queue[0][0]:
		heapq.heappop(self._queue)
		heapq.heappush(self._queue, (-posting.term_frequency, posting.doc_id, posting))