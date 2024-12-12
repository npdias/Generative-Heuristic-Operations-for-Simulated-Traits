# ~infrastructure/coordinator.py

import logging
from infrastructure.services.chat_handler import ChatHandler
from infrastructure.services.memory_handler import MemoryHandler
from infrastructure.models.conversation import Conversation


class Coordinator:
    def __init__(self):
        self.chat_handler = ChatHandler()
        self.memory_handler = MemoryHandler()

    async def start_session(self):
        logging.info("Starting session...")
        await self.chat_handler.fetch_chat_history()
        await self.memory_handler.initialize()

    async def end_session(self):
        logging.info("Ending session...")
        logging.info("Generating chat history...")

        # Generate the transcript from ChatHandler
        transcript = await self.chat_handler.generate_transcript()

        # Create and register the Conversation memory
        conversation = await self.memory_handler.create_memory(Conversation, transcript=transcript)

        # Summarize the conversation
        await self.memory_handler.summarize_conversation(conversation)

        logging.info("Session ended successfully.")
