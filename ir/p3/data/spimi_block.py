from dataclasses import dataclass
from typing import List, Dict
from ir.p3.data.posting import Posting


@dataclass
class Block:
    index: Dict[str, List[Posting]]
    sorted_terms: list
    name: str
