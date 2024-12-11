from dataclasses import dataclass, field
from typing import List, Dict, Any
from infrastructure.models import *


@dataclass
class Person(Memory):
    name: str  # Required field (no default)
    relation: str  # Required field (no default)
    alive: bool = field(default=None)  # Default values come after required fields
    isSelf: bool = field(default=False)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    currentObjectives: List[Any] = field(default_factory=list)
    miscDetails: List[Any] = field(default_factory=list)
    personality: str = field(default_factory=str)

    def __post_init__(self):
        self.mem_type = "Person"  # Call Memory's init with mem_type
        super().__post_init__()  # Add to Memory.all_memories
        if self.relation.lower() == 'self':
            self.isSelf = True
            Memory.identity = self

    def __setattr__(self, name, value):
        if self.isSelf:
            Event(note=f'My {name} changed from "{getattr(self, name)}" to "{value}"')
        self.__dict__[name] = value