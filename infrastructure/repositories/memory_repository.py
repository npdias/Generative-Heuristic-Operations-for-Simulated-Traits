import aiofiles
import os
import json
import logging
from domain.models import Memory


MEMORY_FILE = "data/memories.json"


class MemoryRepository:
    @staticmethod
    async def load_memories(file_location: str = MEMORY_FILE) -> bool:
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
                        logging.debug("Loaded memory: %s", memory_data)
                    else:
                        logging.warning("Unknown memory type: %s", mem_type)
                logging.info("Successfully loaded all memories.")
                return True
        except FileNotFoundError:
            logging.warning(f"No memory file found at {file_location}.")
            return False
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON: %s", e)
            return False
        except Exception as e:
            logging.error("Unexpected error while loading memories: %s", e)
            return False

    @staticmethod
    async def save_memories(file_location: str):
        """
        Save all memories to a JSON file asynchronously.

        Args:
            file_location (str): Path to the JSON file.
        """
        try:
            os.makedirs(os.path.dirname(file_location), exist_ok=True)
            async with aiofiles.open(file_location, mode="w") as file:
                data = {"memories": [memory.__dict__ for memory in Memory.all_memories]}
                await file.write(json.dumps(data, indent=4))
                logging.info(f"Successfully saved memories to {file_location}.")
        except Exception as e:
            logging.error(f"Failed to save memories: {e}")


