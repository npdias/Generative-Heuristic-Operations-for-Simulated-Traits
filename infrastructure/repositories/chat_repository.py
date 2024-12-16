"""
chat_repository.py
==================
This module manages the persistence and retrieval of chat logs. It provides
methods to handle chat interactions, store them in a JSON file, and retrieve
or clear chat logs as needed.

Key Responsibilities:
- Load chat logs from a JSON file.
- Save chat logs to persistent storage.
- Add, retrieve, and clear chat logs.

Classes:
- `ChatRepository`: Core class for managing chat log storage.

Example Usage:
```python
from infrastructure.repositories import ChatRepository

repo = ChatRepository()
await repo.load_chat()
await repo.add_chat({"role": "user", "content": "Hello!"})
chat_logs = repo.load_chat_log()
await repo.clear_chat()
```
"""

import aiofiles
import json
import logging
from typing import List, Dict
import os
from datetime import datetime
from config import DATA_DIR


class ChatRepository:
    """
    Repository for managing chat logs. Responsible for caching chat interactions
    in memory and persisting them to a JSON file.

    Attributes:
        chat_log (List[Dict[str, str]]): In-memory cache for chat logs.
        file_location (str): Path to the JSON file used for chat log storage.
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
                logging.warning("Chat file not found at %s. Starting with an empty log.", self.file_location)
                self.chat_log = []
                return False

            async with aiofiles.open(self.file_location, mode="r") as file:
                data = await file.read()
                if not data.strip():  # Handle empty file
                    logging.warning("Chat file is empty at %s. Starting with an empty log.", self.file_location)
                    self.chat_log = []
                    return False

                self.chat_log = json.loads(data)
                logging.info("Successfully loaded %d chat entries from %s.", len(self.chat_log), self.file_location)
                return True
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON in chat file: %s", e, exc_info=True)
            self.chat_log = []  # Reset to empty if decoding fails
            return False
        except Exception as e:
            logging.error("Unexpected error while loading chat logs: %s", e, exc_info=True)
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
                logging.info("Successfully saved %d chat entries to %s.", len(self.chat_log), self.file_location)
        except Exception as e:
            logging.error("Failed to save chat interactions: %s", e, exc_info=True)
            raise

    def load_chat_log(self) -> List[Dict[str, str]]:
        """
        Retrieve the current in-memory chat log.

        Returns:
            List[Dict[str, str]]: The current chat log as a list of messages.
        """
        logging.debug("Retrieving in-memory chat log with %d entries.", len(self.chat_log))
        return self.chat_log

    async def add_chat(self, message: Dict[str, str]) -> None:
        """
        Add a new chat message to the in-memory chat log and persist it.

        Args:
            message (Dict[str, str]): The chat message to add, including role and content.
        """
        message_with_timestamp = {
            **message,
            "timestamp": datetime.now().isoformat()
        }
        self.chat_log.append(message_with_timestamp)
        logging.info("Added message to chat log: %s", message_with_timestamp)
        await self.save_chat()

    async def clear_chat(self):
        """
        Clear the current chat log and persist the empty state to the JSON file.
        """
        logging.info("Clearing the chat log.")
        self.chat_log = []  # Clear in-memory chat log
        await self.save_chat()
