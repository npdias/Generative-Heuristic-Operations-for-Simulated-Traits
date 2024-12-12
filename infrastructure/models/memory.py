# ~infrastructure/models/memory.py

import uuid
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class Memory:
    """
    Base class representing a generic memory instance.

    Attributes:
        mem_type (str): A string indicating the type of memory (e.g. "Person", "Event").
        ID (str): A unique identifier for the memory.
        entryDate (float): A timestamp (in seconds since epoch) indicating when the memory was created.
    """
    mem_type: str
    ID: str = field(default_factory=lambda: uuid.uuid4().hex)
    entryDate: float = field(default_factory=lambda: time.time())

