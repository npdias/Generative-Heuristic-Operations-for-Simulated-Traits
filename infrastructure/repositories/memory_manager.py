import json
from typing import List, Dict, Any
import os
from config import DATA_DIR
from pathlib import Path
from infrastructure.models import Memory, Person, Event, Conversation
from infrastructure.services.logging_service import memory_manager_logger
import time

class MemoryManager:
    def __init__(self):
        self.logger = memory_manager_logger
        self.file_path = Path(os.path.join(DATA_DIR, 'memories.json'))
        self.memories: List[Dict[str, Any]] = []
        self.memory_ids = set()
        self.self_person = None
        self.load_memories()
        self.misc_details_collection: List[Dict[str, Any]] = []
        self.logger.info(f"MemoryManager initialized. File path: {self.file_path}")

    def load_memories(self):
        """
        Load memories from the JSON file into memory and initialize caches.
        Handles errors related to malformed JSON or unexpected file content.
        """
        if not self.file_path.exists():
            self.logger.warning("Memory file does not exist. Creating a blank file.")
            self.file_path.write_text(json.dumps({"memories": []}, indent=4))

        try:
            self.logger.info(f"Attempting to load JSON file: {self.file_path}")
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                # self.logger.debug(f"Raw JSON content: {data}")
                self.memories = data["memories"]
                self.memory_ids = {mem["ID"] for mem in self.memories}
                self.self_person = next(
                    (Person(**mem) for mem in self.memories if mem.get("mem_type") == "Person" and mem.get("isSelf")),
                    None
                )
                self.logger.info("Successfully loaded memories.")
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decoding error: {e}")

        except ValueError as e:
            self.logger.error(f"Value error in JSON structure: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error reading JSON: {e}", exc_info=True)



    def _save_memories(self):
        """
        Save the current memory list to the JSON file.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump({"memories": self.memories}, file, indent=4)
            self.logger.info("Memories successfully saved to file.")
        except Exception as e:
            self.logger.critical(f"Failed to save memories to file: {e}", exc_info=True)

    def add_memory(self, memory: Memory):
        """
        Add a new memory if it doesn't already exist.
        Automatically updates the JSON file.
        """
        if memory.ID in self.memory_ids:
            self.logger.info(f"Memory with ID {memory.ID} already exists. Skipping.")
            return

        # Serialize the memory object
        memory_dict = memory.__dict__
        self.memories.append(memory_dict)
        self.memory_ids.add(memory.ID)

        # Cache self_person if applicable
        if isinstance(memory, Person) and memory.isSelf:
            self.self_person = memory

        # Save to file
        self._save_memories()

    def get_identity(self) -> Person:
        """
        Retrieve the cached self Person object.
        """
        self.logger.info("Retrieved self person from cache.")
        return self.self_person

    def _add_misc_details(self, fact:dict):
        self.misc_details_collection.append(fact)


    async def get_all_memories(self):
        # Separate Conversations from other memory types
        conversations = [memory for memory in self.memories if memory['mem_type'] == 'Conversation']
        other_memories = [memory for memory in self.memories if memory['mem_type'] != 'Conversation']
        # Find the most recent Conversation
        convo_trimmed = []
        if conversations:
            most_recent_conversation = max(conversations, key=lambda c: c['entryDate'])
            self._add_misc_details(dict(last_conversation={key: value for key, value in most_recent_conversation.items() if key not in  {"transcript","ID"}}))
            for c in conversations:
                if c is most_recent_conversation:
                    convo_trimmed.append(c)
                else:
                    convo_trimmed.append({key: value for key, value in c.items() if key != "transcript"})
        else:
            most_recent_conversation = None

        # Combine modified Conversations and other memories into one list
        all_memories = convo_trimmed + other_memories
        return all_memories
