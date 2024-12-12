# ~infrastructure/repositories/memory_repository.py

import os
import json
import logging
import aiofiles
from typing import List
from config import DATA_DIR

# Import memory classes
from infrastructure.models.memory import Memory
from infrastructure.models.event import Event
from infrastructure.models.fact import Fact
from infrastructure.models.person import Person
from infrastructure.models.conversation import Conversation


class MemoryRepository:
    """
    Repository for managing memory logs. Responsible for caching memory instances in memory
    and persisting them to a JSON file.
    """

    def __init__(self, file_name: str = "memories.json"):
        self.memories: List[Memory] = []  # In-memory cache of Memory instances
        self.file_location = os.path.join(DATA_DIR, file_name)

        # Mapping from mem_type strings to classes
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
                logging.warning(f"Memory file not found at {self.file_location}. Starting with an empty list.")
                self.memories = []
                return False

            async with aiofiles.open(self.file_location, mode="r") as file:
                data = await file.read()
                json_data = json.loads(data)
                if not json_data:  # Handle empty file
                    logging.warning(f"Memory file is empty at {self.file_location}. Starting with an empty list.")
                    self.memories = []
                    return False



                for obj in json_data['memories']:
                    class_obj = self.class_mapping[obj['mem_type']](**obj)
                    self.memories.append(class_obj)
                logging.info(f"Successfully loaded memories from {self.file_location}.")
                return True
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON in memory file: {e}")
            self.memories = []
            return False
        except Exception as e:
            logging.error(f"Unexpected error while loading memories: {e}")
            self.memories = []
            return False

    async def save_all(self):
        """
        Persist the current list of memories to the JSON file.

        Raises:
            Exception: If the file cannot be written due to IO errors.
        """
        print(self.memories)
        try:
            os.makedirs(os.path.dirname(self.file_location), exist_ok=True)
            async with aiofiles.open(self.file_location, mode="w") as file:
                data = {"memories": [obj.__dict__ for obj in self.memories]}
                print(data)
                await file.write(json.dumps(data, indent=4))
                logging.info(f"Successfully saved memories to {self.file_location}.")
        except Exception as e:
            logging.error(f"Failed to save memories: {e}")
            raise

    def get_all_memories(self) -> List[Memory]:
        """
        Retrieve the current in-memory list of memories.

        Returns:
            List[Memory]: The current list of Memory instances.
        """
        return self.memories

    async def append_and_save_all(self, memory: Memory) -> None:
        """
        Add a new memory to the in-memory list and persist it.

        Args:
            memory (Memory): The memory instance to add.
        """
        self.memories.append(memory)
        logging.info(f"add_memory called. Current memories: {[m for m in self.memories]}")
        await self.save_all()

    async def clear_all_memories(self):
        """
        # Clear the current list of memories and persist the empty state.
        # """
        # logging.info("Clearing all memories...")
        # self.memories = []
        # await self.save_all()

    def _memory_to_dict(self, memory: Memory) -> dict:
        """
        Convert a Memory instance to a dictionary suitable for JSON serialization.

        Args:
            memory (Memory): The memory instance to convert.

        Returns:
            dict: A dictionary representation of the memory.
        """
        return {field: getattr(memory, field) for field in memory.__dir__()}
