import aiofiles
import json
import logging
from domain.models import Memory


# Define default file locations for JSON storage
MEMORY_FILE = "data/memories.json"

# Memory Repository
class MemoryRepository:
    @staticmethod
    async def load_memories(file_location: str = MEMORY_FILE):
        """
        Load memories from a JSON file asynchronously.

        Args:
            file_location (str): Path to the JSON file.

        Returns:
            bool: True if memories were successfully loaded, False otherwise.
        """
        try:
            async with aiofiles.open(file_location, mode="r") as file:
                data = await file.read()
                memories = json.loads(data).get("memories", [])
                for memory_data in memories:
                    mem_type = memory_data.pop("mem_type", None)
                    class_mapping = Memory.get_class_mapping()
                    if mem_type in class_mapping:
                        class_mapping[mem_type](**memory_data)
                logging.info("Successfully loaded memories.")
                return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load memories: {e}")
            return False

    @staticmethod
    async def save_memories(file_location: str = MEMORY_FILE):
        """
        Save all memories to a JSON file asynchronously.

        Args:
            file_location (str): Path to the JSON file.
        """
        try:
            async with aiofiles.open(file_location, mode="w") as file:
                data = {"memories": [memory.__dict__ for memory in Memory.all_memories]}
                await file.write(json.dumps(data, indent=4))
                logging.info("Successfully saved memories.")
        except Exception as e:
            logging.error(f"Failed to save memories: {e}")