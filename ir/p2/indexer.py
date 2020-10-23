import argparse
import pickle
import time
from ir.p1 import solutions
from ir.p2 import stream_filters

preprocessings = []
terms = 0
postings = 0
tokens = 0

def create_index(terms, output_index):
    index = {}
    for term in terms:
        if not term[1] in index:
            index[term[1]] = [term[0]]
        else:
            index[term[1]].append(term[0])

    terms, postings = (count_terms(index), count_postings(index))
    print('terms: {}\tpostings: {}\ttokens: {}'.format(terms, postings, tokens))

    with open(output_index, 'wb') as f:
        pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)


def parse_document(path, stopwords):
    stream = stream_filters.tokenizer(
            solutions.block_extractor(
                solutions.block_document_segmenter(
                    solutions.block_reader(path)
                )
            )
        )

    for filter in preprocessings:
        stream = filter(stream, stopwords)

    global tokens
    stream = list(stream)
    tokens = count_tokens(stream)

    return sorted(set(stream), key=lambda element: (element[1], element[0]))

def count_terms(index):
    return len(index)

def count_postings(index):
    count = 0
    for key in index:
        count += len(index[key])
    return count

def count_tokens(terms):
    return len(terms)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Reuters')
    parser.add_argument('-p', '--path', help='Reuters collection directory')
    parser.add_argument('-i', '--index', help="The index outputfile")
    parser.add_argument('-s', '--stopwords', help="remove the stopwords in the given list from the index", default=None)
    parser.add_argument('-rmn', '--removenumbers', help="remove numbers from the index", action='store_true')
    parser.add_argument('-cf', '--casefolding', help="case fold the terms before indexing them", action='store_true')
    parser.add_argument('-st', '--stemming', help="stem the terms before indexing them", action='store_true')

    args = parser.parse_args()

    if args.removenumbers:
        preprocessings.append(stream_filters.remove_numbers)
    if args.casefolding:
        preprocessings.append(stream_filters.case_folding)
    if args.stopwords is not None:
        preprocessings.append(stream_filters.remove_stopwords)
        args.stopwords = open(args.stopwords, 'r').read()
    if args.stemming:
        preprocessings.append(stream_filters.stem)

    start_time = time.time()
    create_index(
        parse_document(args.path, args.stopwords)
        ,args.index
    )
    stop_time = time.time()
    print('process finished in {}s'.format(stop_time-start_time))