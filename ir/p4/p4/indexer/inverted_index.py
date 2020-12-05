from dataclasses import dataclass
from typing import Dict

from ir.p4.p4.indexer.postings_list import PostingsList


@dataclass
class InvertedIndex:
    inverted_index: Dict[str, PostingsList]
