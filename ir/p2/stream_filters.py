import string
from ir.p1.solutions import block_stemmer
from nltk.tokenize import RegexpTokenizer

def remove_numbers(stream, *args):
    for token in stream:
        # if not any([character.isnumeric() for character in token[1]]):
        if not token[1].isnumeric():
            yield(token[0], token[1])

def case_folding(stream, *args):
    for token in stream:
        yield (token[0], token[1].lower())

def remove_stopwords(stream, *args):
    stopwords = args[0]
    stopwords = [] if stopwords == None else [word.lower() for word in stopwords.split()]
    for tup in stream:
        if not tup[1] in stopwords:
            yield (tup[0], tup[1])

def tokenizer(stream, *args):
    tokenizer = RegexpTokenizer('[A-Za-z]+|[0-9]+')
    for document in stream:
        for word in tokenizer.tokenize(document['TEXT']):
            yield(document['ID'], word)

def stem(stream, *args):
    return block_stemmer(stream)