import pickle
import argparse
import sys
import json
from nltk import PorterStemmer

def query_term(terms, index_file, output_file, stem_query):
    stemmer = PorterStemmer()
    index = load_index(index_file)
    result = {}
    for term in terms:
        term_to_query = term
        if stem_query and not contains_uppercase(term):
            term_to_query = stemmer.stem(term)
        result[term] = index[term_to_query] if term_to_query in index else []
    print(json.dumps(result, indent=3), file=output_file)

def contains_uppercase(word):
    return any([character.isupper() for character in word])
def load_index(index_file):
    with open(index_file, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query a dictionary term')
    parser.add_argument('-i', '--index', help="The inverted index to use", required=True)
    parser.add_argument('-t', '--terms', help="A list of terms to perform single term queries on", metavar='term', required=True, nargs='+')
    parser.add_argument('-o', '--output', help="The path for the output file", default=sys.stdout, required=False)
    parser.add_argument('-st', '--stemming', help="whether to stem the query terms, use if the index was created on stemmed tokens", action='store_true')

    args = parser.parse_args()

    if type(args.output) is str:
        args.output = open(args.output, 'w', encoding='utf-8')

    query_term(args.terms, args.index, args.output, args.stemming)