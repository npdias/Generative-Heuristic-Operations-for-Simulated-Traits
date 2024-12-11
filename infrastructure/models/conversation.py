from dataclasses import dataclass
from .memory import Memory

@dataclass
class Conversation(Memory):
    transcript: str
    summary: str

    def __post_init__(self):
        self.mem_type = 'Conversation'
        super().__post_init__()  # Add to Memory.all_memories
