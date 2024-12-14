"""
memory.py
=========
This module defines the `Memory` base class, which serves as the foundation for
different types of memories, such as events, facts, conversations, and persons.

Key Responsibilities:
- Provide a common structure for memory objects.
- Automatically generate unique identifiers and timestamps for each instance.
- Serve as the base class for specialized memory types.

Classes:
- `Memory`: Base class for all memory types.

Example Usage:
```python
from infrastructure.models.memory import Memory

memory = Memory(mem_type="Generic")
print(memory)
```
"""

import uuid
import time
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class Memory:
    """
    Base class representing a generic memory instance.

    Attributes:
        mem_type (str): A string indicating the type of memory (e.g., "Person", "Event").
        ID (str): A unique identifier for the memory.
        entryDate (float): A timestamp (in seconds since epoch) indicating when the memory was created.
    """
    mem_type: str
    ID: str = field(default_factory=lambda: uuid.uuid4().hex)
    entryDate: float = field(default_factory=lambda: time.time())

    def __str__(self):
        """
        Returns a formatted string representation of the memory.

        Returns:
            str: A string showing the memory type and ID.
        """
        return f"[{self.mem_type}] ID: {self.ID}, Entry Date: {self.entryDate}"
