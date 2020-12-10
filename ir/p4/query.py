import argparse
import math
import pickle

from ir.p4.p4.indexer.data.inverted_index import InvertedIndex
from ir.p4.p4.indexer.data.postings_list import PostingsList


def query(index_file):
    index: InvertedIndex = pickle.load(open(index_file, "rb"))

    for term in index.inverted_index:
        print(f'term {term}, df:{index.inverted_index[term].get_document_frequency()}')
        for posting in index.inverted_index[term].get_postings():
            print(f'\t{posting}')

    for document in index.document_list:
        print(f'document: {document.id}, size: {document.size}')

    print(f'nb: {index.document_list.get_nb_documents()}, avg: {index.document_list.get_average_document_length()}')


def tf_idf_ranking(index: InvertedIndex):
    postings: PostingsList = PostingsList()
    for term in index.inverted_index:
        postings_list = index.inverted_index[term]
        for posting in postings_list.get_postings():
            pass


def tf_idf_score(term_frequency, document_frequency, nb_documents):
    return (
        (1 + math.log(term_frequency)) +
        math.log(nb_documents/document_frequency)
    )


def bm25_score(document_frequency, term_frequency, nb_documents, document_length, average_document_length, k1, b):
    return math.log(nb_documents/document_frequency)*(
            ((k1+1)*term_frequency)/
            (k1*((1-b)+b*(document_length/average_document_length)+term_frequency))
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('-i', '--index', help="Path to the inverted index to use", type=str, default="index/index_big.pickle")
    args = parser.parse_args()

    query(args.index)
