"""
event.py
========
This module defines the `Event` class, a specialized type of memory for storing
information about significant occurrences. Events can include associated dates
and detailed notes.

Key Responsibilities:
- Represent event memories with notes and date-related fields.
- Extend the base `Memory` class with specific attributes for events.
- Provide methods for a clear textual representation.

Classes:
- `Event`: Memory subclass for storing event-related information.

Example Usage:
```python
from infrastructure.models.event import Event

event = Event(
    note="Attended a workshop on AI ethics.",
    dates=["2024-12-13"]
)
print(event)
```
"""

from dataclasses import dataclass, field
from typing import List, Any
from infrastructure.models.memory import Memory

@dataclass(kw_only=True)
class Event(Memory):
    """
    Represents an event memory with attributes such as notes and associated dates.

    Attributes:
        mem_type (str): Specifies the type of memory, default is 'Event'.
        note (str): A descriptive note about the event.
        dates (List[Any]): A list of dates associated with the event.
    """
    mem_type: str = field(default="Event")
    note: str
    dates: List[Any] = field(default_factory=list)

    def __str__(self):
        """
        Returns a formatted string representation of the event.

        Returns:
            str: A string showing the note and associated dates.
        """
        dates_str = ", ".join(str(date) for date in self.dates) if self.dates else "None"
        return f"[{self.mem_type}] Note: {self.note}, Dates: {dates_str}"
