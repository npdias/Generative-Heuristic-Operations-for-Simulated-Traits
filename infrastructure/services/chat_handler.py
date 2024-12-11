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
        """
        Process user input by querying the LLM and returning responses.

        Args:
            user_input (str): The user's input.
            stream (bool): Whether to stream the response.

        Yields:
            str: The assistant's response in chunks if streaming, otherwise the complete response.
        """
        logging.info("Processing user input through ChatHandler: %s", user_input)

        # Construct messages with prior context
        prior_context = self.chat_repository.load_chat_log()
        messages = [
            *prior_context,  # Include prior chat context
            {"role": "user", "content": user_input}
        ]

        # Query the LLM and yield results
        if stream:
            logging.info("Streaming response enabled.")
            async for chunk in self.llm_service.send_completion(messages, stream=True):
                yield chunk
        else:
            logging.info("Non-streaming response requested.")
            response = ""
            async for chunk in self.llm_service.send_completion(messages, stream=False):
                response += chunk
            # Save user input and assistant response
            await self.chat_repository.add_chat({"role": "user", "content": user_input})
            await self.chat_repository.add_chat({"role": "assistant", "content": response})
            yield response

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
        logging.info("generating chat history...")
        # Retrieve the current chat history
        chat_history = self.chat_repository.load_chat_log()
        if not chat_history:
            logging.warning("Chat history is empty, nothing to summarize.")
            return {"summary": "", "transcript": ""}
        # Format the transcript
        transcript = "\n".join(f"[{msg['role'].capitalize()}]: {msg['content']}" for msg in chat_history)
        await Conversation(transcript=transcript)
        return True

