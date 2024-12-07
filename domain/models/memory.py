import uuid
import time

class Memory:
    """
    Base class for representing a memory.
    Keeps track of all memory instances and provides common functionality for derived classes.
    """
    all_memories = []
    identity = None

    def __init__(self, mem_type=None):
        self.ID = uuid.uuid4().hex
        self.mem_type = mem_type
        self.entryDate = time.time()
        self.add_to_memory()

    def add_to_memory(self):
        Memory.all_memories.append(self)

    def __str__(self):
        return f"Memory(ID={self.ID}, type={self.mem_type})"
