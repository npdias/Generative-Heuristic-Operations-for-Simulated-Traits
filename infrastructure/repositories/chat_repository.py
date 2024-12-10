#acts as cache for chat - all this can do is read and write

import aiofiles
import json
import logging
from typing import List, Dict
import os
from datetime import datetime
from config import DATA_DIR



class ChatRepository:
    """
    Repository for managing chat interactions.
    """

    def __init__(self):
        """
        Initialize the ChatRepository.
        """
        self.chat_log: List[Dict[str, str]] = []  # Ensure chat_log is initialized as an empty list
        self.file_location = os.path.join(DATA_DIR, 'chat.json')

    async def load_chat(self) -> bool:
        """
        Load interactions from a JSON file asynchronously.

        Args:
            self.file_location (str): Path to the JSON file.

        Returns:
            bool: True if interactions were loaded successfully, False otherwise.
        """
        try:
            async with aiofiles.open(self.file_location, mode="r") as file:
                data = await file.read()
                self.chat_log = json.loads(data)  # Load interactions into chat_log
                logging.info(f"Successfully loaded chat interactions from {self.file_location}.")
                return True
        except FileNotFoundError:
            logging.warning(f"No chat file found at {self.file_location}.")
            self.chat_log = []  # Reset chat_log to an empty list if file is missing
            return False
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            self.chat_log = []  # Reset chat_log to an empty list if decoding fails
            return False

    async def save_chat(self):
        """
        Save all interactions to a JSON file asynchronously.

        Args:
            self.file_location (str): Path to the JSON file.
        """
        try:
            os.makedirs(os.path.dirname(self.file_location), exist_ok=True)  # Ensure directory exists
            async with aiofiles.open(self.file_location, mode="w") as file:
                await file.write(json.dumps(self.chat_log, indent=4))
                logging.info(f"Successfully saved chat interactions to {self.file_location}.")
        except Exception as e:
            logging.error(f"Failed to save chat interactions: {e}")


    def load_chat_log(self) -> List[Dict[str, str]]:
        """
        Retrieve the loaded chat log as a list of messages.

        Returns:
            list: The chat log.
        """
        return self.chat_log

    async def add_chat(self, message: Dict[str, str]) -> None:
        """
        Add a new message to the chat log and save it.

        Args:
            message (Dict[str, str]): A dictionary with "role" and "content".
        """
        message_with_timestamp = {
            **message,
            "timestamp": datetime.now().isoformat()  # Use UTC timestamp
        }
        self.chat_log.append(message_with_timestamp)
        logging.info(f"Added new message to chat log: {message_with_timestamp}")
