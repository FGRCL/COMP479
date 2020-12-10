from dataclasses import dataclass


@dataclass
class Term:
    term: str = ''
    tf: int = 0
    df: int = 0
