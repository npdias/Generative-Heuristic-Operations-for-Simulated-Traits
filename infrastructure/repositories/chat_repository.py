import aiofiles
import json
import logging
from typing import List, Dict
import os
from datetime import datetime
from config import DATA_DIR


class ChatRepository:
    """
    Repository for managing chat logs. Responsible for caching chat interactions in memory
    and persisting them to a JSON file.
    """

    def __init__(self):
        """
        Initialize the ChatRepository with an empty chat log and file location.
        """
        self.chat_log: List[Dict[str, str]] = []  # In-memory cache for chat logs
        self.file_location = os.path.join(DATA_DIR, 'chat.json')

    async def load_chat(self) -> bool:
        """
        Load chat logs from the JSON file into memory.

        Returns:
            bool: True if chat logs were successfully loaded, False otherwise.
        """
        try:
            if not os.path.exists(self.file_location):
                logging.warning(f"Chat file not found at {self.file_location}. Starting with an empty log.")
                self.chat_log = []
                return False

            async with aiofiles.open(self.file_location, mode="r") as file:
                data = await file.read()
                if not data.strip():  # Handle empty file
                    logging.warning(f"Chat file is empty at {self.file_location}. Starting with an empty log.")
                    self.chat_log = []
                    return False

                self.chat_log = json.loads(data)
                logging.info(f"Successfully loaded chat interactions from {self.file_location}.")
                return True
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON in chat file: {e}")
            self.chat_log = []  # Reset to empty if decoding fails
            return False
        except Exception as e:
            logging.error(f"Unexpected error while loading chat logs: {e}")
            self.chat_log = []  # Reset to empty on any other error
            return False

    async def save_chat(self):
        """
        Persist the current chat log to the JSON file.

        Raises:
            Exception: If the file cannot be written due to IO errors.
        """
        try:
            os.makedirs(os.path.dirname(self.file_location), exist_ok=True)  # Ensure directory exists
            async with aiofiles.open(self.file_location, mode="w") as file:
                await file.write(json.dumps(self.chat_log, indent=4))
                logging.info(f"Successfully saved chat interactions to {self.file_location}.")
        except Exception as e:
            logging.error(f"Failed to save chat interactions: {e}")
            raise

    def load_chat_log(self) -> List[Dict[str, str]]:
        """
        Retrieve the current in-memory chat log.

        Returns:
            List[Dict[str, str]]: The current chat log as a list of messages.
        """
        return self.chat_log

    async def add_chat(self, message: Dict[str, str]) -> None:
        message_with_timestamp = {
            **message,
            "timestamp": datetime.now().isoformat()
        }
        self.chat_log.append(message_with_timestamp)
        logging.info(f"add_chat called. Current chat log: {self.chat_log}")
        await self.save_chat()

    async def clear_chat(self):
        """
        Clear the current chat log and persist the empty state to the JSON file.
        """
        logging.info("Clearing the chat log...")
        self.chat_log = []  # Clear in-memory chat log
        await self.save_chat()  # Save the cleared state
