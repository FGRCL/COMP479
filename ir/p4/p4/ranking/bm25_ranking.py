import math

from ir.p4.p4.ranking.ranking_algorithm import RankingAlgorithm


class BM25Ranking(RankingAlgorithm):
    def __init__(cls, nb_documents_to_return):
        super().__init__(nb_documents_to_return)

    def score(self, document_frequency, term_frequency, nb_documents, document_length, average_document_length, k1, b):
        return math.log(nb_documents / document_frequency) * (
                ((k1 + 1) * term_frequency) /
                (k1 * ((1 - b) + b * (document_length / average_document_length) + term_frequency))
        )
