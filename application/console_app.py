"""
console_app.py
==============
This module provides a console-based interface for interacting with the application.
It allows users to send input, receive responses, and manage sessions directly
from the command line.

Key Responsibilities:
- Initialize and manage the console application.
- Handle user input and display responses from the assistant.
- Support session start, end, and clean shutdown.

Classes:
- `ConsoleApp`: Main class for managing the console interface.

Example Usage:
```python
from application.console_app import ConsoleApp

app = ConsoleApp()
app.run()
```
"""

import asyncio
import logging
from application.coordinator import Coordinator

class ConsoleApp:
    """
    Provides a console-based interface for interacting with the assistant.

    Attributes:
        coordinator (Coordinator): Handles the core workflows and interactions.
    """

    def __init__(self):
        """
        Initialize the ConsoleApp with a Coordinator instance.
        """
        self.coordinator = Coordinator()

    async def run(self):
        """
        Start the console application, managing user input and assistant responses.
        """
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
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    app = ConsoleApp()
    asyncio.run(app.run())