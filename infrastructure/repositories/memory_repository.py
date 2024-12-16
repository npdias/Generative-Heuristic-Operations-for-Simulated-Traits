"""
memory_repository.py
====================
This module manages the persistence and retrieval of memory objects. It handles
interactions with the underlying storage system, ensuring that memory data is
safely stored and retrieved for use in the application.

Key Responsibilities:
- Load memory data from a JSON file into memory.
- Save the current state of memory objects to a JSON file.
- Provide methods to clear, append, and retrieve memories.

Classes:
- `MemoryRepository`: Core class for managing memory storage.

Example Usage:
```python
from infrastructure.repositories import MemoryRepository

repo = MemoryRepository()
await repo.load_all()
memories = repo.get_all_memories()
await repo.clear_all_memories()
```
"""

import os
import json
import logging
import aiofiles
from typing import List
from infrastructure import Memory, Event, Fact, Person, Conversation
from config import DATA_DIR

class MemoryRepository:
    """
    Repository for managing memory objects. Provides mechanisms to persist and
    retrieve memories from a JSON file.

    Attributes:
        file_location (str): Path to the JSON file used for memory storage.
        memories (List[Memory]): In-memory cache of memory objects.
        class_mapping (dict): Maps memory types to their corresponding classes.
    """

    def __init__(self, file_name: str = "memories.json"):
        """
        Initialize the repository with a file location and an empty memory cache.

        Args:
            file_name (str): The name of the file used for storing memories.
        """
        self.memories: List[Memory] = []  # In-memory cache of Memory instances
        self.file_location = os.path.join(DATA_DIR, file_name)
        self.class_mapping = {
            "Person": Person,
            "Event": Event,
            "Fact": Fact,
            "Conversation": Conversation,
        }

    async def load_all(self) -> bool:
        """
        Load all memories from the JSON file into memory.

        Returns:
            bool: True if memories were successfully loaded, False otherwise.
        """
        try:
            if not os.path.exists(self.file_location):
                logging.warning("Memory file not found at %s. Starting with an empty list.", self.file_location)
                self.memories = []
                return False

            async with aiofiles.open(self.file_location, mode="r") as file:
                data = await file.read()
                json_data = json.loads(data) if data.strip() else {}

                if not json_data:
                    logging.warning("Memory file is empty at %s. Starting with an empty list.", self.file_location)
                    self.memories = []
                    return False

                for obj in json_data.get('memories', []):
                    class_obj = self.class_mapping[obj['mem_type']]
                    memory_instance = class_obj(**obj)
                    self.memories.append(memory_instance)

                logging.info("Successfully loaded %d memories from %s.", len(self.memories), self.file_location)
                return True
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON in memory file: %s", e, exc_info=True)
            self.memories = []
            return False
        except Exception as e:
            logging.error("Unexpected error while loading memories: %s", e, exc_info=True)
            self.memories = []
            return False

    async def save_all(self):
        """
        Persist the current list of memories to the JSON file.

        Raises:
            Exception: If the file cannot be written due to IO errors.
        """
        try:
            os.makedirs(os.path.dirname(self.file_location), exist_ok=True)
            async with aiofiles.open(self.file_location, mode="w") as file:
                data = {"memories": [obj.__dict__ for obj in self.memories]}
                await file.write(json.dumps(data, indent=4))
                logging.info("Successfully saved %d memories to %s.", len(self.memories), self.file_location)
        except Exception as e:
            logging.error("Failed to save memories: %s", e, exc_info=True)
            raise

    def get_all_memories(self) -> List[Memory]:
        """
        Retrieve the current in-memory list of memories.

        Returns:
            List[Memory]: The current list of Memory instances.
        """
        logging.debug("Retrieving in-memory list of %d memories.", len(self.memories))
        return self.memories

    async def append_and_save_all(self, memory: Memory) -> None:
        """
        Add a new memory to the in-memory list and persist it.

        Args:
            memory (Memory): The memory instance to add.
        """
        self.memories.append(memory)
        logging.info("Added memory of type '%s' to in-memory cache.", memory.mem_type)
        await self.save_all()

    async def clear_all_memories(self):
        """
        Clear all memories from the system and persist the empty state.
        """
        logging.info("Clearing all memories from the repository.")
        self.memories = []
        await self.save_all()
