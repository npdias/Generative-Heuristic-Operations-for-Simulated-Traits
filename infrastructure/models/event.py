from dataclasses import dataclass, field
from typing import List, Any
from .memory import Memory

@dataclass
class Event(Memory):
    note: str
    dates: List[Any] = field(default=None)

    def __post_init__(self):
        self.mem_type = 'Event'
        super().__post_init__()  # Add to Memory.all_memories
