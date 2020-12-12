from dataclasses import dataclass, field
from typing import List, Dict

from ir.p4.p4.ranking.data.term import Term


@dataclass
class Index:
    documents: Dict[str, List[Term]] = field(default_factory=lambda: {})

    def insert(self, doc_id, term, tf, df):
        if doc_id not in self.documents:
            self.documents[doc_id] = []
        self.documents[doc_id].append(Term(term, tf, df))

    def __iter__(self) -> str:
        yield from self.documents

    def __getitem__(self, doc_id):
        return self.documents[doc_id]