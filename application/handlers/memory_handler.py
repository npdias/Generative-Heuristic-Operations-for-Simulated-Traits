"""
memory_handler.py
=================
This module orchestrates memory-related workflows, including initialization,
summarization, and registration of memories. It interacts with the memory repository
for storage and retrieval while leveraging the LLM for generating summaries.

Key Responsibilities:
- Initialize memory state and ensure default memories are present.
- Summarize existing memories using the LLM.
- Create and register new memory instances.
- Provide access to stored memories.

Classes:
- `MemoryHandler`: Core class for managing memory workflows.

Example Usage:
```python
from infrastructure.services import MemoryHandler

memory_handler = MemoryHandler()
await memory_handler.initialize()
summary = await memory_handler.summarize_memories()
print(summary)
```
"""

import asyncio
import logging
from typing import List, Type

from infrastructure import Memory, Event, Fact, Person, Conversation
from infrastructure import MemoryRepository
from infrastructure import LLMService
from config import DEFAULT_MEM_PROMPT, DEFAULT_CONVO_PROMPT

class MemoryHandler:
    """
    The MemoryHandler orchestrates the lifecycle of memory objects:
    - Initializes the memory state from the MemoryRepository.
    - Ensures a default memory is present if none exist.
    - Provides a single method to create and register new memories.
    - Offers a summarization feature by interacting with the LLMService.

    Attributes:
        repository (MemoryRepository): Handles storage and retrieval of memories.
        memories (List[Memory]): Cached list of loaded memory objects.
        llm_service (LLMService): Interacts with the LLM for summarization tasks.
    """

    def __init__(self, file_name: str = "memories.json"):
        """
        Initialize the MemoryHandler with a MemoryRepository and an LLMService instance.

        Args:
            file_name (str): The name of the file where memories are stored.
        """
        self.repository = MemoryRepository(file_name=file_name)
        self.memories: List[Memory] = []
        self.llm_service = LLMService()

    async def initialize(self):
        """
        Load memories from the repository and ensure a default memory is present if none exist.
        """
        logging.info("Initializing MemoryHandler.")

        await self.repository.load_all()
        self.memories = self.repository.get_all_memories()
        logging.debug("Loaded %d memories from repository.", len(self.memories))

        if not self.memories:
            logging.info("No memories found. Creating a default Person memory.")
            await self.add_memory(Person, {'name': "Default", 'relation': "self", 'isSelf': True, 'alive': True})

    async def add_memory(self, cls: Type[Memory], kwarg_dict: dict) -> Memory:
        """
        Create and add a new memory instance of the given subclass of Memory.

        Args:
            cls (Type[Memory]): The subclass of Memory to instantiate.
            kwarg_dict (dict): Fields required by the memory subclass.

        Returns:
            Memory: The newly created memory instance.
        """
        if not issubclass(cls, Memory):
            raise ValueError("cls must be a subclass of Memory")

        try:
            memory = cls(**kwarg_dict)
            await self.repository.append_and_save_all(memory)
            self.memories = self.repository.get_all_memories()
            logging.info("Added new memory: %s", memory)
            return memory
        except Exception as e:
            logging.error("Failed to add memory: %s", e, exc_info=True)
            raise

    async def clear_all_memories(self):
        """
        Clear all memories from the system.
        """
        logging.info("Clearing all memories.")
        await self.repository.clear_all_memories()
        self.memories = []

    async def summarize_memories(self, content: str = '', prompt: str = DEFAULT_MEM_PROMPT) -> str:
        """
        Generate a summary of all currently loaded memories using the LLMService.

        Args:
            content (str): Specific content to summarize, defaults to all memories if empty.
            prompt (str): Custom prompt to guide the LLM.

        Returns:
            str: A textual summary of all memories.
        """
        content = content if content else str(self.memories)
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]

        summary = ""
        try:
            logging.info("Generating memory summary using LLM.")
            async for chunk in self.llm_service.send_completion(messages=messages, stream=False):
                summary += chunk
            logging.debug("Generated memory summary: %s", summary)
        except Exception as e:
            logging.error("Failed to generate memory summary: %s", e, exc_info=True)
            summary = "Error: Unable to generate summary."

        return summary

    async def summarize_conversation(self, transcript: str) -> Memory:
        """
        Generate a summary for a specific conversation and add it to memories.

        Args:
            transcript (str): The transcript of the conversation.

        Returns:
            Memory: The updated conversation with the summary.
        """
        if not transcript:
            logging.warning("No transcript provided for summarization.")
            summary = "No transcript provided."
            conversation = await self.add_memory(Conversation, {'transcript': "", 'summary': summary})
            return conversation

        logging.info("Summarizing conversation transcript.")
        summary = await self.summarize_memories(content=transcript, prompt=DEFAULT_CONVO_PROMPT)
        conversation = await self.add_memory(Conversation, {'transcript': transcript, 'summary': summary})
        logging.info("Conversation summarized and added to memories.")
        return conversation

    def get_memories(self) -> List[Memory]:
        """
        Retrieve the current list of memories in-memory.

        Returns:
            List[Memory]: The in-memory list of Memory instances.
        """
        logging.debug("Retrieving in-memory list of %d memories.", len(self.memories))
        return self.memories.copy()
