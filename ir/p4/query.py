import argparse
import pickle
import sys

from ir.p4.p4.indexer.data.inverted_index import InvertedIndex
from ir.p4.p4.indexer.tokenizer import tokenize_text
from ir.p4.p4.ranking.ranking_algorithm_choice import RankingAlgorithmChoice
from ir.p4.p4.ranking.ranking_algorithm import RankingAlgorithm


def query(index_file: str, query: str, ranking_algorithm_choice: RankingAlgorithmChoice):

    inverted_index: InvertedIndex = pickle.load(open(index_file, "rb"))

    ranking: RankingAlgorithm = ranking_algorithm_choice.get_algorithm()
    query_tokens = list(tokenize_text(query))
        
    ranked_documents = ranking.rank(query_tokens, inverted_index)

    for i, ranked_document in enumerate(ranked_documents):
        print(f'rank: {i+1} \tscore: {ranked_document[0].__round__(4)}\tdocument:{ranked_document[1]}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('--index', '-i', help="Path to the inverted index to use", type=str, default="index/index_big.pickle")
    parser.add_argument('--query', '-q', help="the use query", type=str, required=True)
    parser.add_argument('--rankingalgorithm', '-ra', help="The ranking algorithm to use", choices=RankingAlgorithmChoice, type=RankingAlgorithmChoice.from_string, default=RankingAlgorithmChoice.tfidf)
    parser.add_argument('--output', '-o', help="The output file", type=str, required=False)
    args = parser.parse_args()

    if args.output is not None:
        sys.stdout = open(args.output, "w")

    query(args.index, args.query, args.rankingalgorithm)
