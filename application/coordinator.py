"""
coordinator.py
===============
This module orchestrates the high-level workflows of the application by coordinating
interactions between chat and memory handlers. It acts as the bridge between the
application's components, ensuring seamless workflows.

Key Responsibilities:
- Manage session workflows (start, end, and in-session processes).
- Integrate memory management with chat interactions.
- Maintain application state consistency across components.

Classes:
- `Coordinator`: The primary class responsible for orchestrating the workflows.

Example Usage:
```python
from infrastructure.services import Coordinator

coordinator = Coordinator()
await coordinator.start_session()
await coordinator.end_session()
```
"""

import logging
from application.handlers import ChatHandler, MemoryHandler
from config import *

class Coordinator:
    """
    Orchestrates workflows between chat and memory handlers.

    Attributes:
        chat_handler (ChatHandler): Handles chat interactions and manages chat logs.
        memory_handler (MemoryHandler): Manages memory initialization, retrieval, and summarization.
    """

    def __init__(self):
        """
        Initialize the Coordinator with necessary handlers.
        """
        self.chat_handler = ChatHandler()
        self.memory_handler = MemoryHandler()

    async def start_session(self):
        """
        Start a session by initializing handlers and generating a memory summary.
        """
        logging.info("Session start initiated.")
        await self.chat_handler.fetch_chat_history()
        await self.memory_handler.initialize()

        logging.info("Fetching memory summary.")
        summary = await self.memory_handler.summarize_memories()
        cur_objectives = self.memory_handler.identity.currentObjectives
        initial_prompt = f"{INITIAL_PROMPT} **Memory:** {summary} **Other tracked objectives:** {cur_objectives}"
        await self.chat_handler.add_chat_passthrough(role='system', content=initial_prompt)

        logging.info("Session start completed.")

    async def end_session(self):
        """
        End a session by generating and summarizing the chat history.
        """
        logging.info("Session end initiated.")

        # Generate the transcript from ChatHandler
        logging.info("Generating chat transcript.")
        transcript = await self.chat_handler.generate_transcript()

        # Create and register the Conversation memory
        logging.info("Summarizing conversation.")
        await self.memory_handler.summarize_conversation(transcript)

        logging.info("Session end completed successfully.")
