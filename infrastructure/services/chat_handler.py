"""
chat_handler.py
===============
This module manages chat interactions, coordinating workflows with the language model (LLM)
and storing chat histories. It acts as an intermediary between user input and the LLM's output,
handling context management and response generation.

Key Responsibilities:
- Process user input and manage context.
- Interact with the LLM for generating responses.
- Store and retrieve chat history.
- Support both streaming and non-streaming responses.

Classes:
- `ChatHandler`: Core class for managing chat workflows.

Example Usage:
```python
from infrastructure.services.chat_handler import ChatHandler

chat_handler = ChatHandler()
response = await chat_handler.process_user_input("Hello!", stream=True)
async for chunk in response:
    print(chunk)
```
"""

import asyncio
import logging
from typing import AsyncGenerator, List, Dict

from infrastructure.models import Conversation
from infrastructure.repositories.chat_repository import ChatRepository
from infrastructure.services.llm_service import LLMService

class ChatHandler:
    """
    Manages chat interactions, coordinating workflows and interactions with the LLM
    and the chat repository.

    Attributes:
        chat_repository (ChatRepository): Handles chat storage and retrieval.
        llm_service (LLMService): Interacts with the language model for responses.
    """

    def __init__(self):
        """
        Initialize the ChatHandler with a ChatRepository and an LLMService instance.
        """
        self.chat_repository = ChatRepository()
        self.llm_service = LLMService()

    async def process_user_input(self, user_input: str, stream: bool = False) -> AsyncGenerator[str, None]:
        """
        Process user input by sending it to the LLM and storing the resulting response.

        Args:
            user_input (str): The user's input message.
            stream (bool): Whether to enable streaming responses.

        Yields:
            str: Response chunks in streaming mode or the full response in non-streaming mode.
        """
        logging.info("Starting to process user input: '%s'", user_input)

        try:
            # Add the user message to the chat log
            await self.chat_repository.add_chat({"role": "user", "content": user_input})
            logging.debug("User input added to chat log.")

            # Retrieve updated context
            prior_context = self.chat_repository.load_chat_log()
            logging.debug("Loaded chat context with %d messages.", len(prior_context))

            messages = prior_context

            if stream:
                logging.info("Streaming response mode enabled.")
                assistant_response = ""
                async for chunk in self.llm_service.send_completion(messages, stream=True):
                    assistant_response += chunk
                    yield chunk
                logging.debug("Streaming response complete. Final response length: %d characters.", len(assistant_response))

                # Store the complete assistant response
                await self.chat_repository.add_chat({"role": "assistant", "content": assistant_response})
                logging.info("Assistant response stored successfully.")
            else:
                logging.info("Non-streaming response mode selected.")
                assistant_response = ""
                async for chunk in self.llm_service.send_completion(messages, stream=False):
                    assistant_response += chunk
                logging.debug("Non-streaming response generated. Final response length: %d characters.", len(assistant_response))

                # Store the complete assistant response
                await self.chat_repository.add_chat({"role": "assistant", "content": assistant_response})
                logging.info("Assistant response stored successfully.")
                yield assistant_response
        except Exception as e:
            logging.error("Error while processing user input: %s", e, exc_info=True)
            yield "Error: Unable to process the input."

    async def add_chat_passthrough(self, role: str, content: str):
        """
        Directly add a chat message to the repository.

        Args:
            role (str): The role of the message sender (e.g., 'assistant').
            content (str): The content of the message.
        """
        logging.info("Adding passthrough message to chat log.")
        await self.chat_repository.add_chat({"role": role, "content": content})

    async def fetch_chat_history(self) -> List[Dict[str, str]]:
        """
        Retrieve the current chat history.

        Returns:
            List[Dict[str, str]]: The list of chat interactions.
        """
        logging.info("Fetching chat history.")
        return self.chat_repository.load_chat_log()

    async def clear_chat_history(self):
        """
        Clear the current chat history in the repository.
        """
        logging.info("Clearing chat history.")
        self.chat_repository.chat_log.clear()
        await self.chat_repository.save_chat()

    async def generate_transcript(self) -> str:
        """
        Generate a formatted transcript of the chat history.

        Returns:
            str: The formatted transcript.
        """
        logging.info("Generating chat transcript.")

        # Retrieve the current chat history
        chat_history = self.chat_repository.load_chat_log()
        if not chat_history:
            logging.warning("Chat history is empty.")
            return ""

        # Format the transcript
        transcript = "\n".join(
            f"[{msg['role'].capitalize()}]: {msg['content']}" for msg in chat_history
        )
        logging.info("Chat transcript generated.")
        return transcript
