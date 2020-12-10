from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from ir.p4.p4.indexer.data.inverted_index import InvertedIndex
from ir.p4.p4.indexer.data.token import Token
from ir.p4.p4.ranking.data.index import Index
from ir.p4.p4.ranking.ranked_document_queue import RankedDocumentsQueue


class RankingAlgorithm(ABCMeta):
    def __init__(cls, nb_documents_to_return):
        super().__init__(cls)
        cls._nb_documents_to_return = nb_documents_to_return

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
            ranked_documents.insert_posting(rank, doc_id)

        return ranked_documents.get_ranked_posting()

    @abstractmethod
    def score(self, document_frequency, term_frequency, nb_documents, document_length, average_document_length, k1, b):
        raise NotImplemented
