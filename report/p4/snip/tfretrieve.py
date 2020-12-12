def get_postings(self) -> List[Posting]:
	return [element[2] for element in heapq.nsmallest(self._max_items, self._queue)]