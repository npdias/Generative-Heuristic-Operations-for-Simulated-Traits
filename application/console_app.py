# ~application/console_app.py

import asyncio
import logging
from infrastructure.coordinator import Coordinator

class ConsoleApp:
    def __init__(self):
        self.coordinator = Coordinator()

    async def run(self):
        logging.info("Starting ConsoleApp...")

        # Ensure the session starts before entering the loop
        await self.coordinator.start_session()
        logging.info("Session started. Entering the main loop.")

        print("Welcome to the Chat Console!")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() in ['exit', 'quit']:
                print("Exiting chat. Goodbye!")
                await self.coordinator.end_session()
                break

            print("Assistant: ", end="", flush=True)

            # Stream the response
            async for chunk in self.coordinator.chat_handler.process_user_input(user_input, stream=True):
                print(chunk, end="", flush=True)
            print("\n")  # Add a newline after the response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    app = ConsoleApp()
    asyncio.run(app.run())
