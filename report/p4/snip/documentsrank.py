def rank(self, query: List[Token], inverted_index: InvertedIndex) -> List[Tuple[float, str]]:
	index: Index = Index()
	for query_token in query:
		postings = inverted_index.get_postings(query_token.term)
		df = postings.get_document_frequency()
		for posting in postings:
			index.insert(posting.doc_id, query_token.term, posting.term_frequency, df)

	nb_documents = inverted_index.document_list.get_nb_documents()
	average_document_length = inverted_index.document_list.get_average_document_length()
	ranked_documents: RankedDocumentsQueue = RankedDocumentsQueue(self._nb_documents_to_return)
	for doc_id in index:
		document_length = inverted_index.document_list.get_document(doc_id).size
		rank = 0
		for term in index[doc_id]:
			rank += self.score(term.df, term.tf, nb_documents, document_length, average_document_length, 0.5, 1)
		ranked_documents.insert_document(rank, doc_id)

	return ranked_documents.get_ranked_posting()