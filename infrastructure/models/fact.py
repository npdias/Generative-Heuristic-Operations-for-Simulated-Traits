from dataclasses import dataclass
from .memory import Memory

@dataclass
class Fact(Memory):
    source: str
    note: str

    def __post_init__(self):
        self.mem_type = 'Fact'
        super().__post_init__()  # Add to Memory.all_memories
