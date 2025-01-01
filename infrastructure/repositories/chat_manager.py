import json
import time
from config import DATA_DIR
import os
from infrastructure.services.logging_service import chat_manager_logger


class ChatManager:
    def __init__(self):
        """
        Initializes the ChatManager with a file path to store/read chat logs.
        """
        self.logger = chat_manager_logger
        self.file_path = os.path.join(DATA_DIR, 'chat.json')
        self.transcript = []

        # Load existing chats from the file into memory
        # self.load_transcript()

    def load_transcript(self):
        """
        Loads the transcript from the file.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.transcript = [{key: value for key, value in message.items()} for message in data]
        except FileNotFoundError:
            self.transcript = []
        except json.JSONDecodeError:
            self.logger.error("Error reading JSON file. The file may be corrupted.")

    def save_transcript(self):
        """
        Saves the in-memory transcript to the file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.transcript, file, indent=4)

    def add_message(self, role, content):
        """
        Adds a new message to the transcript.
        """
        self.transcript.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        self.logger.debug(f"Add Message:\trole:{role}\tcontent:{content}")
        self.save_transcript()

    def add_response(self, response):
        """
        Takes formatted json from api response and adds a new message to the transcript.
        """
        self.transcript.append(response)
        self.logger.debug(f"Message Directly added (add_response):\tcontent:{response}")
        self.save_transcript()

    def get_transcript(self, trimmed:bool = False):
        """
        Returns the in-memory transcript or trimmed version of in-memory transcript without system msg
        """
        if self.transcript:
            if not trimmed:
                return self.transcript
            else:
                return [c for c in self.transcript if c['role'] != 'system']

    def clear_transcript(self):
        self.transcript = []
        self.save_transcript()
