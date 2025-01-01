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

    Example:
        An example of creating an Event instance:

        ```python
        event = Event(note="Team meeting", dates=["2025-01-01", "2025-01-02"])
        print(event)
        ```

        This could represent a scheduled team meeting over two days.
    """
    note: str
    dates: List[Any] = field(default_factory=list)
    mem_type: str = field(default="Event")

    def __str__(self):
        """
        Returns a formatted string representation of the event.

        Returns:
            str: A string showing the note and associated dates.
        """
        dates_str = ", ".join(str(date) for date in self.dates) if self.dates else "None"
        return f"[{self.mem_type}] Note: {self.note}, Dates: {dates_str}"
