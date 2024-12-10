import logging
from infrastructure.services.llm_service import LLMService
from infrastructure.repositories.chat_repository import ChatRepository
from infrastructure.repositories.memory_repository import MemoryRepository

class Orchestrator:
    """
    Orchestrator for managing workflows between services, repositories, and user interactions.
    """

    def __init__(self):
        self.llm_service = LLMService()
        self.chat_repository = ChatRepository()
        self.memory_repository = MemoryRepository()

    async def start_session(self):
        """
        Start a new session.
        """
        logging.info("Starting a new session...")
        await self.chat_repository.load_chat()
        await self.memory_repository.load_memories()

    async def handle_user_input(self, user_input: str, stream: bool = False):
        """
        Handle user input by querying the LLM and saving the interaction.

        Args:
            user_input (str): The user's input.
            stream (bool): Whether to stream the response.

        Returns:
            str or generator: The assistant's response.
        """
        # Construct messages with system context
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            *self.chat_repository.load_chat_log(),  # Include prior chat context
            {"role": "user", "content": user_input}
        ]

        logging.info("Handling user input: %s", user_input)

        # Query the LLM
        if stream:
            return self.llm_service.send_completion(messages, stream=True)
        else:
            response = self.llm_service.send_completion(messages, stream=False)
            # Save the interaction to the chat log
            await self.chat_repository.add_chat({"role": "user", "content": user_input})
            await self.chat_repository.add_chat({"role": "assistant", "content": response})
            return response

    async def end_session(self):
        """
        End the session and save all interactions to memory.
        """
        logging.info("Ending session and saving data...")
        await self.chat_repository.save_chat()
        await self.memory_repository.save_memories()

import asyncio

if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    async def main():
        orchestrator = Orchestrator()

        # Start a new session
        await orchestrator.start_session()

        # Handle user input
        user_input = "Explain the concept of gravity."
        print("\nNon-Streaming Response:")
        response = await orchestrator.handle_user_input(user_input)
        print(response)

        # Handle user input with streaming
        print("\nStreaming Response:")
        async for chunk in orchestrator.handle_user_input("Describe the water cycle.", stream=True):
            print(chunk, end="", flush=True)

        # End the session
        await orchestrator.end_session()

    asyncio.run(main())
