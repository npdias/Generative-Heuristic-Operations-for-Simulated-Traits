import asyncio
import logging
from typing import AsyncGenerator, List, Dict

from infrastructure.models import Conversation
from infrastructure.repositories.chat_repository import ChatRepository
from infrastructure.services.llm_service import LLMService


class ChatHandler:
    """
    Manages chat interactions, coordinating workflows and interactions with LLM and the chat repository.
    """

    def __init__(self):
        """
        Initialize the ChatHandler with a ChatRepository and an LLMService instance.
        """
        self.chat_repository = ChatRepository()
        self.llm_service = LLMService()

    async def process_user_input(self, user_input: str, stream: bool = False) -> AsyncGenerator[str, None]:
        logging.info("Processing user input through ChatHandler: %s", user_input)

        # First, add the user message to the chat log
        await self.chat_repository.add_chat({"role": "user", "content": user_input})

        # Now retrieve the updated context
        prior_context = self.chat_repository.load_chat_log()

        # For the request to LLM, the prior_context now includes the newly added user message
        messages = prior_context

        if stream:
            logging.info("Streaming response enabled.")
            assistant_response = ""
            # Stream the response from LLM
            async for chunk in self.llm_service.send_completion(messages, stream=True):
                assistant_response += chunk
                yield chunk

            # After streaming is complete, add the assistant's full response
            await self.chat_repository.add_chat({"role": "assistant", "content": assistant_response})

        else:
            logging.info("Non-streaming response requested.")
            assistant_response = ""
            async for chunk in self.llm_service.send_completion(messages, stream=False):
                assistant_response += chunk

            # Add the assistant's response to the log
            await self.chat_repository.add_chat({"role": "assistant", "content": assistant_response})
            logging.debug(f"Response added to chat log: {assistant_response}")
            yield assistant_response

    async def add_chat_passthrough(self, role, content):
        await self.chat_repository.add_chat({"role": "assistant", "content": content})

    async def fetch_chat_history(self) -> List[Dict[str, str]]:
        """
        Retrieve the current chat history.

        Returns:
            List[Dict[str, str]]: The list of chat interactions from the repository.
        """
        logging.info("Fetching chat history...")
        return self.chat_repository.load_chat_log()

    async def clear_chat_history(self):
        """
        Clear the current chat history in the repository.
        """
        logging.info("Clearing chat history...")
        self.chat_repository.chat_log.clear()
        await self.chat_repository.save_chat()

    async def generate_transcript(self):
        from infrastructure.models.conversation import Conversation
        logging.info("Generating chat history...")

        # Retrieve the current chat history from in-memory cache
        chat_history = self.chat_repository.load_chat_log()
        if not chat_history:
            logging.warning("Chat history is empty, nothing to summarize.")
            return None

        # Format the transcript as a string
        transcript = "\n".join(
            f"[{msg['role'].capitalize()}]: {msg['content']}"
            for msg in chat_history
        )

        # Return the created transcript object
        return transcript

