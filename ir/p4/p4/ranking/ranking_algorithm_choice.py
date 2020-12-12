from enum import Enum

from ir.p4.p4.ranking.bm25_ranking import BM25Ranking
from ir.p4.p4.ranking.ranking_algorithm import RankingAlgorithm
from ir.p4.p4.ranking.tf_idf_ranking import TfIdfRanking


class RankingAlgorithmChoice(Enum):
    tfidf = TfIdfRanking(15)
    bm25 = BM25Ranking(15)

    def __init__(self, algorithm: RankingAlgorithm):
        self._algorithm = algorithm

    def __str__(self):
        return self.name

    def get_algorithm(self):
        return self._algorithm

    @staticmethod
    def from_string(name):
        return RankingAlgorithmChoice[name]