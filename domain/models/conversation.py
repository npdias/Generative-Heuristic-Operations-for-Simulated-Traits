from dataclasses import dataclass
from .memory import Memory

@dataclass
class Conversation(Memory):
    transcript: str
    summary: str

    def __post_init__(self):
        super().__init__(mem_type='Conversation')
