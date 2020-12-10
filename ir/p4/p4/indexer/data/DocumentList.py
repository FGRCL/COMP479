from dataclasses import dataclass, field
from typing import Dict

from ir.p4.p4.indexer.data.Document import Document


@dataclass
class DocumentList:
    document_dictionary: Dict[str, Document] = field(default_factory=lambda: {})

    def get_document(self, doc_id: str) -> Document:
        if doc_id not in self.document_dictionary:
            self.document_dictionary[doc_id] = Document(doc_id, 0)
        return self.document_dictionary[doc_id]

    def get_average_document_length(self) -> float:
        return sum([self.document_dictionary[document].size for document in self.document_dictionary])/self.get_nb_documents()

    def get_nb_documents(self) -> int:
        return len(self.document_dictionary)

    def __iter__(self) -> Document:
        for doc_id in self.document_dictionary:
            yield self.document_dictionary[doc_id]