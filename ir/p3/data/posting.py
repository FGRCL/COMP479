from dataclasses import dataclass


@dataclass
class Posting:
    doc_id: str
    term_frequency: int
