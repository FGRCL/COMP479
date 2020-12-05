import argparse
import heapq
import json
import sys
from enum import Enum
from math import log
from typing import Dict
from ir.p3.util import load_block_from_pickle
from ir.p3.data.spimi_block import Block
from ir.p3.datastructure.doc_rank_queue import RankedDocumentQueue


def query_term(terms, index_file, output_file, query_mode):
    block: Block = load_block_from_pickle(index_file)

    index: Dict = block.index
    document_lengths = block.document_lengths
    collection_size = len(index)
    average_document_length = get_average_document_length(document_lengths)

    result = []
    if query_mode == QueryMode.RANKED:
        ranked_documents: RankedDocumentQueue = RankedDocumentQueue()
        for term in terms:
            if term in index:
                for posting in index[term]:
                    df = len(index[term])
                    tf = posting.term_frequency
                    document_length = document_lengths[posting.doc_id]
                    rank = rank_term(df, tf, collection_size, document_length, average_document_length)
                    ranked_documents.push(posting, rank)
        result = [posting.doc_id for posting in ranked_documents]
    elif query_mode == QueryMode.AND:
        postings_list = []
        first_term = True
        for term in terms:
            if term in index:
                postings_list = intersect_postings(postings_list, index[term], first_term)
                first_term = False
        result = [posting.doc_id for posting in postings_list]
    elif query_mode == QueryMode.OR:
        postings_list = []
        for term in terms:
            if term in index:
                postings_list = postings_list + index[term]
        postings_list.sort(key=lambda p: p.term_frequency, reverse=True)
        result = [posting.doc_id for posting in postings_list]

    print(json.dumps(result, indent=3), file=output_file)


def rank_term(df, tf, collection_size, document_length, average_document_length):
    k = 1
    b = 1
    return log(collection_size/df, 10) * ( ((k+1)*tf) / (k*((1-b)+b*(document_length/average_document_length))+tf) )


def get_average_document_length(document_lengths: Dict[int, int]):
    return sum([document_lengths[key] for key in document_lengths])/len(document_lengths)


def intersect_postings(first_postings, second_postings, first_term):
    intersect_postings = []

    if first_term:
        intersect_postings = second_postings
    else:
        i, j = 0, 0

        while i < len(first_postings) and j < len(second_postings):
            first_doc_id = first_postings[i].doc_id
            second_doc_id = second_postings[j].doc_id
            if first_doc_id < second_doc_id:
                i += 1
            if first_doc_id > second_doc_id:
                j += 1
            if first_doc_id == second_doc_id:
                intersect_postings.append(first_postings[i])
                i += 1
                j += 1

    return intersect_postings


def union_positions(heap, second_postings):
    for postings in second_postings:
        heapq.heappush(heap, (postings.term_frequency, postings.doc_id))


class QueryMode(Enum):
    OR = 1,
    AND = 2,
    RANKED = 3,

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('-i', '--index', help="The inverted index to use", required=True)
    parser.add_argument('-t', '--terms', help="A list of terms to perform single term queries on", metavar='term', required=True, nargs='+')
    parser.add_argument('-o', '--output', help="The path for the output file", default=sys.stdout, required=False)
    parser.add_argument('-m', '--mode', help="", choices=QueryMode, type=lambda x: QueryMode[x], default='RANKED')

    args = parser.parse_args()

    if type(args.output) is str:
        args.output = open(args.output, 'w', encoding='utf-8')

    query_term(args.terms, args.index, args.output, args.mode)
