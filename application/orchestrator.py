import logging
from infrastructure.services.llm_service import LLMService
from infrastructure.repositories.chat_repository import ChatRepository
from infrastructure.repositories.memory_repository import MemoryRepository
from typing import AsyncGenerator, Union
import asyncio

CHAT_FILE = "data/chat.json"
MEMORY_FILE = "data/memories.json"

class Orchestrator:
    def __init__(self):
        self.llm_service = LLMService()
        self.chat_repository = ChatRepository()
        self.memory_repository = MemoryRepository()

    async def start_session(self):
        logging.info("Starting a new session...")
        await self.chat_repository.load_chat(file_location=CHAT_FILE)
        await self.memory_repository.load_memories(file_location=MEMORY_FILE)

    async def handle_user_input(self, user_input: str, stream: bool = False):
        """
        Handle user input by querying the LLM and saving the interaction.

        Args:
            user_input (str): The user's input.
            stream (bool): Whether to stream the response.

        Yields:
            str: The assistant's response in chunks if streaming, otherwise the complete response.
        """
        # Construct messages with system context
        prior_context = self.chat_repository.load_chat_log()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            *prior_context,  # Include prior chat context
            {"role": "user", "content": user_input}
        ]

        logging.info("Handling user input: %s", user_input)

        await self.chat_repository.add_chat({"role": "user", "content": user_input})
        response = ""

        if stream:
            # Stream the response and yield chunks
            async for chunk in self.llm_service.send_completion(messages, stream=True):
                response += chunk
                yield chunk  # Yield chunk for further processing if needed
        else:
            # Non-streaming response
            async for chunk in self.llm_service.send_completion(messages, stream=False):
                response += chunk
            yield response
        await self.chat_repository.add_chat({"role": "assistant", "content": response})

    async def end_session(self):
        logging.info("Ending session and saving data...")
        await self.chat_repository.save_chat(file_location=CHAT_FILE)
        await self.memory_repository.save_memories(file_location=MEMORY_FILE)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


    async def main():
        orchestrator = Orchestrator()

        # Start a new session
        await orchestrator.start_session()

        # Handle user input (Non-Streaming)
        user_input = "Explain the concept of gravity."
        print("\nNon-Streaming Response:")
        async for response in orchestrator.handle_user_input(user_input, stream=False):
            print(response)  # Ensure non-streaming response prints correctly

        # Handle user input with streaming
        print("\nStreaming Response:")
        async for chunk in orchestrator.handle_user_input("Write 3 haikus about Nuns and use the word None as often as you can", stream=True):
            print(chunk, end="", flush=True)  # Ensure streaming chunks print incrementally
        print()

        # End the session
        await orchestrator.end_session()


    asyncio.run(main())
