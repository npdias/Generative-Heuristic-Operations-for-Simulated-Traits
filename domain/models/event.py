from dataclasses import dataclass, field
from typing import List, Any
from .memory import Memory

@dataclass
class Event(Memory):
    note: str
    dates: List[Any] = field(default=None)

    def __post_init__(self):
        super().__init__(mem_type='Event')
