import pickle
import argparse

def query_term(term, index_file):
    index = load_index(index_file)
    result = index[term] if term in index else []
    print(result)
    print(index)

def load_index(index_file):
    with open(index_file, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionnart term')
    parser.add_argument('-i', '--index', help="The index to look into", required=True)
    parser.add_argument('-t', '--term', help="The term to lookup", metavar='term', required=True)

    args = parser.parse_args()
    query_term(args.term, args.index)