import uuid
import time
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class Memory:
    ID: str = field(default_factory=lambda: uuid.uuid4().hex)
    mem_type: str = field(init=False)  # Subclasses will set this
    entryDate: float = field(default_factory=lambda: time.time())

    # Class attribute to track all instances
    all_memories = []
    identity = None

    def add_to_memory(self):
        Memory.all_memories.append(self)

    def __post_init__(self):
        self.add_to_memory()

    def __str__(self):
        return f"Memory(ID={self.ID}, type={self.mem_type})"

    @staticmethod
    def get_class_mapping():
        """
        Returns a dictionary mapping memory types to their corresponding classes.
        """
        from domain.models.person import Person
        from domain.models.event import Event
        from domain.models.fact import Fact
        from domain.models.conversation import Conversation

        return {
            "Person": Person,
            "Event": Event,
            "Fact": Fact,
            "Conversation": Conversation,
        }