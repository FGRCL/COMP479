def insert_posting(self, rank: float, doc_id: str):
	if len(self._queue) < self._max_items:
		heapq.heappush(self._queue, (rank, doc_id))
	elif rank > self._queue[0][0]:
		heapq.heappop(self._queue)
		heapq.heappush(self._queue, (rank, doc_id))
