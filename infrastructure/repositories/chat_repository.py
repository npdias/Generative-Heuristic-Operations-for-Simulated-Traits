import aiofiles
import json
import logging
from domain.models.interaction import Interaction

# Define default file locations for JSON storage
CHAT_FILE = "data/chat.json"


# Chat Repository
class ChatRepository:
    @staticmethod
    async def load_chat(file_location: str = CHAT_FILE):
        """
        Load chat interactions from a JSON file asynchronously.

        Args:
            file_location (str): Path to the JSON file.

        Returns:
            bool: True if interactions were successfully loaded, False otherwise.
        """
        try:
            async with aiofiles.open(file_location, mode="r") as file:
                data = await file.read()
                interactions = json.loads(data)
                Interaction.listed.extend(interactions)
                logging.info("Successfully loaded chat interactions.")
                return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load chat interactions: {e}")
            return False

    @staticmethod
    async def save_chat(file_location: str = CHAT_FILE):
        """
        Save all chat interactions to a JSON file asynchronously.

        Args:
            file_location (str): Path to the JSON file.
        """
        try:
            async with aiofiles.open(file_location, mode="w") as file:
                await file.write(json.dumps(Interaction.listed, indent=4))
                logging.info("Successfully saved chat interactions.")
        except Exception as e:
            logging.error(f"Failed to save chat interactions: {e}")
