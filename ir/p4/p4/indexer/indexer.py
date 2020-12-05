from threading import BoundedSemaphore, Thread
from typing import Union
from urllib.parse import ParseResult, ParseResultBytes

from bs4 import BeautifulSoup

from ir.p3.data.posting import Posting
from ir.p4.p4.indexer.inverted_index import InvertedIndex
from ir.p4.p4.indexer.postings_list import PostingsList
from ir.p4.p4.indexer.tokenizer import tokenize_text


class Indexer:
    def __init__(self):
        self.index = InvertedIndex({})
        self.index_semaphore = BoundedSemaphore()

    def add_document_to_index(self, soup: BeautifulSoup, url: Union[ParseResult, ParseResultBytes]):
        text = soup.get_text()
        doc_id = url.geturl()
        postings = {}
        for token in tokenize_text(text, doc_id):
            if token.term not in postings:
                postings[token.term] = Posting(doc_id, 1)
            else:
                postings[token.term].term_frequency += 1

        for term in postings:
            with self.index_semaphore:
                if term not in self.index.inverted_index:
                    self.index.inverted_index[term] = PostingsList(50)
                self.index.inverted_index[term].insert_posting(postings[term])

    def parse_web_page(self, soup, url):
        thread = Thread(target=self.add_document_to_index, args=(soup, url))
        thread.start()

    def get_index(self) -> InvertedIndex:
        return self.index
