import argparse
import json
import sys
from typing import List
from math import log
from typing import Dict
from ir.p3.util import load_block_from_pickle
from ir.p3.data.posting import Posting
from ir.p3.datastructure.doc_rank_queue import RankedDocumentQueue


def query_term(terms, index_file, output_file):
    index: Dict = load_block_from_pickle(index_file).index
    collection_size = len(index)
    ranked_documents: RankedDocumentQueue = RankedDocumentQueue()
    for term in terms:
        for posting in index[term]:
            df = len(index[term])
            tf = posting.term_count
            rank = rank_term(df, tf, collection_size)
            ranked_documents.push(posting, rank)

    result = [posting.doc_id for posting in ranked_documents]
    print(json.dumps(result, indent=3), file=output_file)


def rank(query: List[Posting]):
    return sum([rank(term) for term in query])


def rank_term(df, tf, collection_size):
    k = 1
    b = 0
    return log(collection_size/df, 10) * ( ((k+1)*tf) / (k*((1-b)+b*(1))+tf) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('-i', '--index', help="The inverted index to use", required=True)
    parser.add_argument('-t', '--terms', help="A list of terms to perform single term queries on", metavar='term', required=True, nargs='+')
    parser.add_argument('-o', '--output', help="The path for the output file", default=sys.stdout, required=False)

    args = parser.parse_args()

    if type(args.output) is str:
        args.output = open(args.output, 'w', encoding='utf-8')

    query_term(args.terms, args.index, args.output)
