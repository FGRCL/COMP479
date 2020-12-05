import argparse
import pickle

from ir.p4.p4.indexer.inverted_index import InvertedIndex


def query(index_file):
    index: InvertedIndex = pickle.load(open(index_file, "rb"))

    for term in index.inverted_index:
        print(f'term {term}, df:{index.inverted_index[term].get_document_frequency()}')
        for posting in index.inverted_index[term].get_postings():
            print(f'\t{posting}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('-i', '--index', help="Path to the inverted index to use", type=str, default="index/index.pickle")
    args = parser.parse_args()

    query(args.index)
