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


class MemoryHandler:
    """
    The MemoryHandler orchestrates the lifecycle of memory objects:
    - Initializes the memory state from the MemoryRepository.
    - Ensures a default memory is present if none exist.
    - Provides utility methods to create and register new memories.
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
            await self.create_default_person()

    async def create_default_person(self):
        """
        Create a default person memory to ensure the system always has at least one memory.
        """
        await self.create_memory(Person, name="Default", relation="self", isSelf=True, alive=True)

    async def create_memory(self, cls: Type[Memory], **kwargs) -> Memory:
        """
        Create a new memory instance of the given subclass of Memory and add it to the repository.

        Args:
            cls (Type[Memory]): The subclass of Memory to instantiate.
            **kwargs: Fields required by the memory subclass.

        Returns:
            Memory: The newly created memory instance.
        """
        if not issubclass(cls, Memory):
            raise ValueError("cls must be a subclass of Memory")

        memory = cls(**kwargs)
        await self.repository.add_memory(memory)
        self.memories = self.repository.get_all_memories()  # Refresh local cache
        return memory

    async def register_memory(self, memory: Memory):
        """
        Register an existing Memory instance with the repository.

        Args:
            memory (Memory): The memory to register.
        """
        if not isinstance(memory, Memory):
            raise ValueError("memory must be an instance of Memory")

        await self.repository.add_memory(memory)
        self.memories = self.repository.get_all_memories()  # Refresh local cache

    async def clear_all_memories(self):
        """
        Clear all memories from the system.
        """
        await self.repository.clear_all_memories()
        self.memories = []

    async def summarize_all_memories(self) -> str:
        """
        Generate a summary of all currently loaded memories using the LLMService.

        Returns:
            str: A textual summary of all memories.
        """
        if not self.memories:
            return "No memories to summarize."

        # Convert memories to a readable format.
        memories_text = "\n".join(self._format_memory(m) for m in self.memories)

        messages = [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": f"Summarize the following memories:\n\n{memories_text}"}
        ]

        summary = ""
        try:
            async for chunk in self.llm_service.send_completion(messages=messages, stream=False):
                summary += chunk
        except Exception as e:
            logging.error(f"Failed to generate summary: {e}")
            summary = "Error: Unable to generate summary."

        return summary

    async def summarize_conversation(self, conversation: Conversation) -> Conversation:
        """
        Generate a summary for a specific conversation and update it.

        Args:
            conversation (Conversation): The conversation to summarize.

        Returns:
            Conversation: The updated conversation with the summary.
        """
        if not conversation.transcript:
            conversation.summary = "No transcript provided."
            await self.repository.save_all()  # Persist the change
            return conversation

        messages = [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": f"Summarize this conversation:\n\n{conversation.transcript}"}
        ]

        summary = ""
        try:
            async for chunk in self.llm_service.send_completion(messages=messages, stream=False):
                summary += chunk
        except Exception as e:
            logging.error(f"Failed to generate summary: {e}")
            summary = "Error: Unable to generate summary."

        conversation.summary = summary
        await self.repository.save_all()  # Persist the change
        return conversation

    def get_memories(self) -> List[Memory]:
        """
        Retrieve the current list of memories in-memory.

        Returns:
            List[Memory]: The in-memory list of Memory instances.
        """
        return self.memories[:]

    def _format_memory(self, memory: Memory) -> str:
        """
        Convert a Memory instance to a readable string format.

        Args:
            memory (Memory): The memory instance to format.

        Returns:
            str: A string representation of the memory.
        """
        if isinstance(memory, Conversation):
            return f"[{memory.mem_type}] Transcript: {memory.transcript}\nSummary: {memory.summary}"
        elif isinstance(memory, Person):
            return f"[{memory.mem_type}] Name: {memory.name}, Relation: {memory.relation}, IsSelf: {memory.isSelf}, Alive: {memory.alive}"
        elif isinstance(memory, Event):
            return f"[{memory.mem_type}] Title: {memory.title}, Description: {memory.description}, Date: {memory.date}"
        elif isinstance(memory, Fact):
            return f"[{memory.mem_type}] Statement: {memory.statement}, Source: {memory.source}"
        else:
            return f"[{memory.mem_type}] ID: {memory.ID}, EntryDate: {memory.entryDate}"
