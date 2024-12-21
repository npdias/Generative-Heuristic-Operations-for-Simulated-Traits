import json
import time
from config import DATA_DIR
import os

class ChatManager:
    def __init__(self):
        """
        Initializes the ChatManager with a file path to store/read chat logs.
        """
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
            print("Error reading JSON file. The file may be corrupted.")

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


# Usage
if __name__ == "__main__":
    chat_manager = ChatManager()

    # # Add messages
    # chat_manager.add_message("system", "Welcome to the chat!")
    # chat_manager.add_message("user", "Hello, system!")

    # Load from Json
    chat_manager.load_transcript()

    # Access in-memory transcript
    print("Transcript in memory:")
    print(chat_manager.get_transcript(trimmed=True))

    # Save transcript to file
    # chat_manager.save_transcript()
