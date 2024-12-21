"""
fact.py

"""

from dataclasses import dataclass, field
from infrastructure.models.memory import Memory

@dataclass(kw_only=True)
class Fact(Memory):
    """
    Represents a factual memory with a source and a descriptive note.

    Attributes:
        source (str): The origin or reference of the fact.
        note (str): A detailed note describing the fact.
    """
    source: str
    note: str
    mem_type: str = field(default="Fact")

    def __str__(self):
        """
        Returns a formatted string representation of the fact.

        Returns:
            str: A string showing the source and note.
        """
        return f"[{self.mem_type}] Source: {self.source}\nNote: {self.note}"
