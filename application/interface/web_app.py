#!/usr/bin/env python3

import logging
import asyncio

from nicegui import ui
from application.coordinator import Coordinator
from application.handlers.log_handler import LogElementHandler  # Reusable log handler

# Initialize Coordinator
coordinator = Coordinator()

# Root logger setup function
def setup_logger(log_component: ui.log) -> None:
    """Configure root logger to send all logs to the NiceGUI log component."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Capture all logs (DEBUG and above)

    # Prevent duplicate handlers
    if not any(isinstance(h, LogElementHandler) for h in root_logger.handlers):
        handler = LogElementHandler(log_component)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        root_logger.addHandler(handler)


class ChatInterface:
    """Handles UI components and chat functionality."""

    def __init__(self):
        self.message_container = None
        self.text_input = None
        self.bot_name = "Bot"

    async def send(self) -> None:
        """Send user input and stream responses from the bot."""
        user_input = self.text_input.value.strip()
        self.text_input.value = ''
        if not user_input:  # Ignore empty inputs
            return

        with self.message_container:
            ui.chat_message(text=user_input, name='You', sent=True)
            response_message = ui.chat_message(name=self.bot_name, sent=False)
            spinner = ui.spinner(type='dots')

        # Stream response from coordinator
        response = ''
        async for chunk in coordinator.chat_handler.process_user_input(user_input, stream=True):
            response += chunk
            response_message.clear()
            with response_message:
                ui.html(response)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

        self.message_container.remove(spinner)

    def setup_ui(self):
        """Define the main user interface."""
        ui.query('.q-page').classes('flex')
        ui.query('.nicegui-content').classes('w-full')

        with ui.tabs().classes('w-full') as tabs:
            chat_tab = ui.tab('Chat')
            logs_tab = ui.tab('Logs')

        with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow'):
            self.message_container = ui.tab_panel(chat_tab).classes('items-stretch')

            with ui.tab_panel(logs_tab):
                log_component = ui.log(max_lines=50).classes('w-full')
                setup_logger(log_component)  # Attach root logger to UI log

        # Footer with input box
        with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
            with ui.row().classes('w-full no-wrap items-center'):
                self.text_input = ui.input(placeholder='Type your message here...').props(
                    'rounded outlined input-class=mx-3'
                ).classes('w-full').on('keydown.enter', self.send)
            ui.markdown('Simple chat app built with [NiceGUI](https://nicegui.io)').classes('text-xs self-end')


# Initialize UI
chat_ui = ChatInterface()


async def startup():
    """Run startup logic asynchronously."""
    logging.info("Starting session asynchronously...")
    await coordinator.start_session()
    identity_dict = await coordinator.get_identity()
    chat_ui.bot_name = identity_dict['name']
    logging.info("Session started.")


@ui.page('/')
async def main():
    """Main page setup."""
    chat_ui.setup_ui()
    asyncio.create_task(startup())  # Start coordinator without blocking


# Run the NiceGUI server
ui.run(title='UI Chat App')
