# domain/models/memory.py
import uuid
import time
import os
import json
import asyncio
import logging
from dataclasses import dataclass, field
import aiofiles  # Ensure this is imported for async file operations
from config import DATA_DIR

@dataclass(kw_only=True)
class Memory:
    """
    Represents a single memory instance and provides functionality to manage all memories.
    """
    ID: str = field(default_factory=lambda: uuid.uuid4().hex)
    mem_type: str = field(init=False)  # Subclasses will set this
    entryDate: float = field(default_factory=lambda: time.time())

    # Class-level attributes for global memory management
    all_memories = []
    identity = {}
    file_location = os.path.join(DATA_DIR, "memories.json")

    def __post_init__(self):
        """
        Perform post-initialization tasks:
        - Add the memory to the global list.
        - Save the memory asynchronously.
        """
        Memory.all_memories.append(self)
        asyncio.create_task(self.save_all_to_file())

    @staticmethod
    async def save_all_to_file():
        """
        Save all memories to the JSON file.
        """
        try:
            os.makedirs(os.path.dirname(Memory.file_location), exist_ok=True)
            async with aiofiles.open(Memory.file_location, mode="w") as file:
                data = {"memories": [memory.__dict__ for memory in Memory.all_memories]}
                await file.write(json.dumps(data, indent=4))
                logging.info(f"Successfully saved memories to {Memory.file_location}.")
        except Exception as e:
            logging.error(f"Failed to save memories: {e}")

    @classmethod
    async def load_from_file(cls):
        """
        Load all memories from the JSON file and instantiate them.
        """
        try:
            async with aiofiles.open(cls.file_location, mode="r") as file:
                data = await file.read()
                if not data.strip():  # Check if the file is empty or contains only whitespace
                    logging.warning(f"The memory file at {cls.file_location} is empty.")
                    return
                memories = json.loads(data).get("memories", [])
                for memory_data in memories:
                    mem_type = memory_data.pop("mem_type", None)
                    class_mapping = cls.get_class_mapping()
                    if mem_type in class_mapping:
                        class_mapping[mem_type](**memory_data)
                    else:
                        logging.warning(f"Unknown memory type: {mem_type}")
                logging.info("Successfully loaded all memories.")
        except FileNotFoundError:
            logging.warning(f"No memory file found at {cls.file_location}.")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while loading memories: {e}")

        if not cls.all_memories:
            logging.info("No memories found. Creating a default Person memory.")
            cls.create_default_person()

    @staticmethod
    def get_class_mapping():
        """
        Returns a dictionary mapping memory types to their corresponding classes.
        """
        from domain.models.person import Person
        from domain.models.event import Event
        from domain.models.fact import Fact
        from domain.models.conversation import Conversation

        return {
            "Person": Person,
            "Event": Event,
            "Fact": Fact,
            "Conversation": Conversation,
        }

    @classmethod
    def create_default_person(cls):
        """
        Create a default `Person` memory representing 'self'.
        """
        from domain.models.person import Person
        Person(name="", relation="self", isSelf=True, alive=True)