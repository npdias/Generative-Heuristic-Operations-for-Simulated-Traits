# ~infrastructure/handler/memory_handler.py

import asyncio


from infrastructure.models.memory import Memory
from infrastructure.models.event import Event
from infrastructure.models.fact import Fact
from infrastructure.models.person import Person
from infrastructure.models.conversation import Conversation



import logging
from typing import List, Type

from infrastructure.repositories.memory_repository import MemoryRepository
from infrastructure.services.llm_service import LLMService
from config import *


class MemoryHandler:
    """
    The MemoryHandler orchestrates the lifecycle of memory objects:
    - Initializes the memory state from the MemoryRepository.
    - Ensures a default memory is present if none exist.
    - Provides a single method to create and register new memories.
    - Offers a summarization feature by interacting with the LLMService.
    """

    def __init__(self, file_name: str = "memories.json"):
        self.repository = MemoryRepository(file_name=file_name)
        self.memories: List[Memory] = []
        self.llm_service = LLMService()  # Instantiate LLMService here

    async def initialize(self):
        """
        Asynchronously load memories from the repository.
        If no memories are found, create a default Person memory.
        """
        await self.repository.load_all()
        self.memories = self.repository.get_all_memories()

        if not self.memories:
            logging.info("No memories found. Creating a default Person memory.")
            await self.add_memory(Person, {'name':"Default", 'relation':"self", 'isSelf':True, 'alive':True})

    async def add_memory(self, cls: Type[Memory], kwarg_dict: dict) -> Memory:
        """
        Create and add a new memory instance of the given subclass of Memory.

        Args:
            cls (Type[Memory]): The subclass of Memory to instantiate.
            kwarg_dict: Fields required by the memory subclass.

        Returns:
            Memory: The newly created memory instance.
        """
        if not issubclass(cls, Memory):
            raise ValueError("cls must be a subclass of Memory")

        try:
            # Instantiate the memory object
            memory = cls(**kwarg_dict)
            # Add to repository
            await self.repository.append_and_save_all(memory)
            # Update in-memory cache
            self.memories = self.repository.get_all_memories()
            logging.info(f"Added memory: {memory}")
            return memory
        except Exception as e:
            logging.error(f"Failed to add memory: {e}")
            raise

    async def clear_all_memories(self):
        """
        Clear all memories from the system.
        """
        await self.repository.clear_all_memories()
        self.memories = []
        logging.info("All memories have been cleared.")

    async def summarize_memories(self, content ='', prompt: str = DEFAULT_MEM_PROMPT) -> str:
        """
        Generate a summary of all currently loaded memories using the LLMService.

        Returns:
            str: A textual summary of all memories.
        """
        content = content if content != '' else self.memories
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(content)}
        ]

        summary = ""
        try:
            async for chunk in self.llm_service.send_completion(messages=messages, stream=False):
                summary += chunk
        except Exception as e:
            logging.error(f"Failed to generate summary: {e}")
            summary = "Error: Unable to generate summary."

        logging.info("Generated summary of all memories.")
        return summary



    async def summarize_conversation(self, transcript: str) -> Memory:
        """
        Generate a summary for a specific conversation and add it to memories.

        Args:
            transcript (str): The transcript of the conversation.

        Returns:
            Conversation: The updated conversation with the summary.
        """
        if not transcript:
            logging.warning("No transcript provided for summarization.")
            summary = "No transcript provided."
            conversation = await self.add_memory(Conversation, {'transcript':"", 'summary':summary})
            return conversation

        summary = await self.summarize_memories(content=transcript, prompt=DEFAULT_CONVO_PROMPT)
        conversation = await self.add_memory(Conversation, {'transcript':transcript, 'summary':summary})
        logging.info(f"Summarized conversation: {conversation}")
        return conversation


    def get_memories(self) -> List[Memory]:
        """
        Retrieve the current list of memories in-memory.

        Returns:
            List[Memory]: The in-memory list of Memory instances.
        """
        return self.memories.copy()
