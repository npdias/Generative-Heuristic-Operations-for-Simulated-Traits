"""
person.py
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from infrastructure.models.memory import Memory

@dataclass(kw_only=True)
class Person(Memory):
    """
    Represents a person memory with attributes such as name, relationship, and status.

    Attributes:
        mem_type (str): Specifies the type of memory, default is 'Person'.
        name (str): The name of the individual.
        relation (str): The relationship of the individual to the system.
        alive (bool): Whether the person is alive or not.
        isSelf (bool): Whether this entry represents the system itself.
        relationships (List[Dict[str, Any]]): A list of relationships associated with the person.
        currentObjectives (List[Any]): Current objectives or goals related to the person.
        miscDetails (List[Any]): Miscellaneous details about the person.
        personality (str): A string describing the person's personality traits.
    """
    name: str
    relation: str
    mem_type: str = field(default="Person")
    alive: bool = None
    isSelf: bool = False
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    currentObjectives: List[Any] = field(default_factory=list)
    miscDetails: List[Any] = field(default_factory=list)
    personality: str = field(default_factory=str)

    def __str__(self):
        """
        Returns a formatted string representation of the person.

        Returns:
            str: A string showing the name, relationship, and status.
        """
        return (f"[{self.mem_type}] Name: {self.name}, Relation: {self.relation}, "
                f"IsSelf: {self.isSelf}, Alive: {self.alive}")
