import logging
from infrastructure.services.chat_handler import ChatHandler
from infrastructure.services.llm_service import LLMService


class Coordinator:
    """
    Coordinates workflows between the ConsoleApp and backend services.
    """

    def __init__(self):
        """
        Initialize the Coordinator with required services.
        """
        self.chat_handler = ChatHandler()
        self.llm_service = LLMService()

    async def start_session(self):
        """
        Perform any setup required at the start of a session, such as loading chat history.
        """
        logging.info("Starting a new session...")
        await self.chat_handler.fetch_chat_history()


    async def handle_user_input(self, user_input: str, stream: bool = False):
        """
        Process user input and return responses via the ChatHandler.

        Args:
            user_input (str): The user's input.
            stream (bool): Whether to stream the response.

        Returns:
            str or AsyncGenerator[str, None]: The assistant's response.
        """
        logging.info("Processing user input via ChatHandler.")
        # Delegate processing to ChatHandler
        async for response in self.chat_handler.process_user_input(user_input, stream=stream):
            yield response

    async def end_session(self):
        """
        Perform any cleanup required at the end of a session, such as saving chat history.
        """
        logging.info("Ending session...")
        # await self.chat_handler.save_chat_history()
