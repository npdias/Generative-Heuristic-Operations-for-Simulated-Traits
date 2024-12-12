# ~infrastructure/models/person.py

from dataclasses import dataclass, field
from typing import List, Dict, Any
from infrastructure.models.memory import Memory

@dataclass(kw_only=True)
class Person(Memory):
    mem_type: str = field(default="Person")
    name: str
    relation: str
    alive: bool = None
    isSelf: bool = False
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    currentObjectives: List[Any] = field(default_factory=list)
    miscDetails: List[Any] = field(default_factory=list)
    personality: str = field(default_factory=str)


    def __str__(self):
        return f"[{self.mem_type}] Name: {self.name}, Relation: {self.relation}, IsSelf: {self.isSelf}, Alive: {self.alive}"
