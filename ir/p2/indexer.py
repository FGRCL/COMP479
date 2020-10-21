import argparse
import pickle
from ir.p1 import solutions

preprocessings = []

def create_index(terms, output_index):
    index = {}
    for term in terms:
        print(term)
        if not term[1] in index:
            index[term[1]] = [term[0]]
        else:
            index[term[1]].append(term[0])

    terms, postings, tokens = (count_terms(index), count_postings(index), count_tokens(terms))
    print('terms: {}\tpostings: {}\ttokens: {}'.format(terms, postings, tokens))

    with open(output_index, 'wb') as f:
        pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)


def parse_document(path, stopwords):
    stream = solutions.block_tokenizer(
            solutions.block_extractor(
                solutions.block_document_segmenter(
                    solutions.block_reader(path)
                )
            )
        )

    for filter in preprocessings:
        stream = filter(stream, stopwords)

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

def remove_numbers(stream, *args):
    for token in stream:
        if not any([character.isnumeric() for character in token[1]]):
            yield(token[0], token[1])

def case_folding(stream, *args):
    for token in stream:
        yield (token[0], token[1].lower())

def remove_stopwords(stream, *args):
    return solutions.block_stopwords_removal(stream, args[0])

def stem(stream, *args):
    return solutions.block_stemmer(stream)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Reuters')
    parser.add_argument('-p', '--path', help='Reuters collection directory')
    parser.add_argument('-i', '--index', help="The index outputfile")
    parser.add_argument('-s', '--stopwords', default=None, help='The stopwords to remove')
    parser.add_argument('-rmn', '--removenumbers', action='store_true')
    parser.add_argument('-cf', '--casefolding', action='store_true')
    parser.add_argument('-st', '--stemming', action='store_true')

    args = parser.parse_args()

    if args.removenumbers:
        preprocessings.append(remove_numbers)
    if args.casefolding:
        preprocessings.append(case_folding)
    if args.stemming:
        preprocessings.append(stem)
    if args.stopwords is not None:
        preprocessings.append(remove_stopwords)
        args.stopwords = open(args.stopwords, 'r').read()


    create_index(
        parse_document(args.path, args.stopwords)
        ,args.index
    )