"""
Write your reusable code here.
Main method stubs corresponding to each block is initialized here. Do not modify the signature of the functions already
created for you. But if necessary you can implement any number of additional functions that you might think useful to you
within this script.

Delete "Delete this block first" code stub after writing solutions to each function.

Write you code within the "WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv" code stub. Variable created within this stub are just
for example to show what is expected to be returned. You CAN modify them according to your preference.
"""

from os import listdir
from bs4 import BeautifulSoup
from nltk import word_tokenize, PorterStemmer

def block_reader(path):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for file in [entry for entry in listdir(path) if entry[-4:] == '.sgm']:
        filePath = '{}/{}'.format(path, file)
        with open(filePath, 'r', encoding='latin-1') as f:
            yield f.read()
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_document_segmenter(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for file in INPUT_STRUCTURE:
        remainingContent = file
        startIndex = remainingContent.find('<REUTERS')
        stopIndex = remainingContent.find('<REUTERS', startIndex+1)
        while startIndex != -1:
            if(stopIndex == -1):
                yield remainingContent[startIndex:]
            else:
                yield remainingContent[startIndex: stopIndex-1]
            remainingContent = remainingContent[stopIndex:]
            startIndex = remainingContent.find('<REUTERS')
            stopIndex = remainingContent.find('<REUTERS', startIndex+1)
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_extractor(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    docId = 1
    for document in INPUT_STRUCTURE:
        root = BeautifulSoup(document, "xml")
        textRoot = root.find('TEXT')
        if textRoot.has_attr('TYPE'):
            if textRoot['TYPE'] == 'BRIEF':
                content = textRoot.find('TITLE').text
                yield {"ID": docId, "TEXT": content}
                docId += 1
        else:
            content = textRoot.find('TITLE').text
            content += textRoot.find('BODY').text
            yield {"ID": docId, "TEXT": content}
            docId += 1
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^

def block_tokenizer(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    for dictionnary in INPUT_STRUCTURE:
        for token in word_tokenize(dictionnary['TEXT']):
            yield (dictionnary['ID'], token)
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stemmer(INPUT_STRUCTURE):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    porter = PorterStemmer()
    for tup in INPUT_STRUCTURE:
        yield(tup[0], porter.stem(tup[1]))
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_stopwords_removal(INPUT_STRUCTURE, stopwords):
    # WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv
    porter = PorterStemmer()
    stemmedStopWords = [] if stopwords == None else [porter.stem(word) for word in stopwords.split()]
    for tup in INPUT_STRUCTURE:
        if not tup[1] in stemmedStopWords:
            yield(tup[0], tup[1])
    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^

