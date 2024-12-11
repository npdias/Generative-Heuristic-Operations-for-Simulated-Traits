# domain/models/memory.py
import uuid
import time
import os
import json
import asyncio
import logging
from dataclasses import dataclass, field
import aiofiles  # Required for asynchronous file operations
from config import DATA_DIR


@dataclass(kw_only=True)
class Memory:
    """
    Represents a single memory instance and provides functionality to manage all memories.

    Attributes:
        ID (str): Unique identifier for the memory, auto-generated as a UUID.
        mem_type (str): Memory type, defined by subclasses.
        entryDate (float): Timestamp for when the memory was created.

    Class Attributes:
        all_memories (list): A global collection of all memory instances.
        identity (dict): Holds identity-specific attributes.
        file_location (str): Path to the JSON file for memory storage.
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
        - Add the memory instance to the global memory list.
        - Trigger asynchronous saving of all memories to the file.
        """
        Memory.all_memories.append(self)
        asyncio.create_task(self.save_all_to_file())

    @staticmethod
    async def save_all_to_file():
        """
        Save all memories to the JSON file asynchronously.

        Implements a retry mechanism for transient errors, such as file locks or permissions issues.
        Logs success or error messages based on the result of the operation.
        """
        retries = 3
        for attempt in range(retries):
            try:
                os.makedirs(os.path.dirname(Memory.file_location), exist_ok=True)
                async with aiofiles.open(Memory.file_location, mode="w") as file:
                    data = {"memories": [memory.__dict__ for memory in Memory.all_memories]}
                    await file.write(json.dumps(data, indent=4))
                    logging.info(f"Successfully saved memories to {Memory.file_location}.")
                    return
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed to save memories: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(1)  # Wait before retrying
                else:
                    logging.error("All retries to save memories have failed.")

    @classmethod
    async def load_from_file(cls):
        """
        Load all memories from the JSON file and instantiate them.

        If the file is empty or does not exist, initialize with default data.
        Logs warnings and errors as needed.
        """
        try:
            async with aiofiles.open(cls.file_location, mode="r") as file:
                data = await file.read()
                if not data.strip():
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

        Returns:
            dict: A mapping of memory types (str) to class types.
        """
        from .person import Person
        from .event import Event
        from .fact import Fact
        from .conversation import Conversation

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
        Ensures there is always at least one memory instance.
        """
        from .person import Person
        Person(name="", relation="self", isSelf=True, alive=True)

    @staticmethod
    async def summarize_all_memories():
        """
        Generate a summary of all memories using the LLMService.

        Returns:
            str: A summary of all stored memories.
        """
        from infrastructure.services.llm_service import LLMService

        messages = [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": f"Summarize the following memories and conversation:\n\n{Memory.all_memories}"}
        ]

        summary = ""
        async for chunk in LLMService.send_completion(messages=messages, stream=False):
            summary += chunk
        return summary
