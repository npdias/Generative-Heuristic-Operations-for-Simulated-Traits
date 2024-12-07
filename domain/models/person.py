from dataclasses import dataclass, field
from typing import List, Dict, Any
from .memory import Memory

@dataclass
class Person(Memory):
    name: str
    relation: str
    alive: bool = field(default=None)
    isSelf: bool = field(default=False)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    currentObjectives: List[Any] = field(default_factory=list)
    miscDetails: List[Any] = field(default_factory=list)
    personality: str = field(default_factory=str)

    def __post_init__(self):
        super().__init__(mem_type='Person')
        if self.relation.lower() == 'self':
            self.isSelf = True
            Memory.identity = self
