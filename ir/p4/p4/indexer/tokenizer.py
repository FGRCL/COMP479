from typing import Generator
from ir.p4.p4.indexer.data.token import Token
from nltk.tokenize import word_tokenize


def tokenize_text(text, id) -> Generator[Token, None, None]:
    for word in word_tokenize(text):
        yield Token(word, id)