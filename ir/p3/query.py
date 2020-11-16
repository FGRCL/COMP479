import argparse
import json
import sys
from typing import List
from ir.p3.util import load_block_from_pickle
from ir.p3.data.spimi_block import Block
from ir.p3.data.posting import Posting


def query_term(terms, index_file, output_file):
    index: Block = load_block_from_pickle(index_file).index
    result = {}
    for term in terms:
        term_to_query = term
        result[term] = get_doc_id(index[term_to_query] if term_to_query in index else [])
    print(json.dumps(result, indent=3), file=output_file)


def get_doc_id(postings_list: List[Posting]):
    return [posting.doc_id for posting in postings_list]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('-i', '--index', help="The inverted index to use", required=True)
    parser.add_argument('-t', '--terms', help="A list of terms to perform single term queries on", metavar='term', required=True, nargs='+')
    parser.add_argument('-o', '--output', help="The path for the output file", default=sys.stdout, required=False)

    args = parser.parse_args()

    if type(args.output) is str:
        args.output = open(args.output, 'w', encoding='utf-8')

    query_term(args.terms, args.index, args.output)
