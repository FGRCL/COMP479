import pickle
import argparse
import sys
import json

def query_term(terms, index_file, output_file):
    index = load_index(index_file)
    result = {}
    for term in terms:
        result[term] = index[term] if term in index else []
    print(json.dumps(result, indent=3), file=output_file)

def load_index(index_file):
    with open(index_file, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionnart term')
    parser.add_argument('-i', '--index', help="The index to look into", required=True)
    parser.add_argument('-t', '--terms', help="The terms to lookup", metavar='term', required=True, nargs='+')
    parser.add_argument('-o', '--output', help="The path for the ouput file", default=sys.stdout, required=False)

    args = parser.parse_args()

    if type(args.output) is str:
        args.output = open(args.output, 'w', encoding='utf-8')

    query_term(args.terms, args.index, args.output)