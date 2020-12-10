from dataclasses import dataclass, field
from typing import Dict

from ir.p4.p4.indexer.data.DocumentList import DocumentList
from ir.p4.p4.indexer.data.postings_list import PostingsList


@dataclass
class InvertedIndex:
    max_postings_list_size: int = 50
    inverted_index: Dict[str, PostingsList] = field(default_factory=lambda: {})
    document_list: DocumentList = DocumentList()

    def get_postings(self, term: str) -> PostingsList:
        if term not in self.inverted_index:
            self.inverted_index[term] = PostingsList(self.max_postings_list_size)
        return self.inverted_index[term]
