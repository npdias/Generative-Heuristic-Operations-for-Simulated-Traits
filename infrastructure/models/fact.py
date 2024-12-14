"""
fact.py
=======
This module defines the `Fact` class, a specialized type of memory for storing
factual information. Facts include a source and a descriptive note to provide
context and detail.

Key Responsibilities:
- Represent factual memories with source and note fields.
- Extend the base `Memory` class with specific attributes for facts.

Classes:
- `Fact`: Memory subclass for storing factual information.

Example Usage:
```python
from infrastructure.models.fact import Fact

fact = Fact(
    source="Wikipedia",
    note="The Eiffel Tower was completed in 1889."
)
print(fact)
```
"""

from dataclasses import dataclass, field
from infrastructure.models.memory import Memory

@dataclass
class Fact(Memory):
    """
    Represents a factual memory with a source and a descriptive note.

    Attributes:
        source (str): The origin or reference of the fact.
        note (str): A detailed note describing the fact.
    """
    mem_type: str = field(default="Fact")
    source: str
    note: str

    def __str__(self):
        """
        Returns a formatted string representation of the fact.

        Returns:
            str: A string showing the source and note.
        """
        return f"[{self.mem_type}] Source: {self.source}\nNote: {self.note}"
