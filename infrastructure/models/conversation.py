# ~infrastructure/models/conversation.py

from dataclasses import dataclass, field
from infrastructure.models.memory import Memory

@dataclass(kw_only=True)
class Conversation(Memory):
    mem_type: str = field(default="Conversation", init=False)
    transcript: str
    summary: str = ""

    def __str__(self):
        return f"[{self.mem_type}] Transcript: {self.transcript}\nSummary: {self.summary}"
