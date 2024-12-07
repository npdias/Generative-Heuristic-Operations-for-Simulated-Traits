from dataclasses import dataclass
from .memory import Memory

@dataclass
class Fact(Memory):
    source: str
    note: str

    def __post_init__(self):
        super().__init__(mem_type='Fact')
