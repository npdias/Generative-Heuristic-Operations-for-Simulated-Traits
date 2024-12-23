import gradio as gr
import asyncio
import logging

from infrastructure.services.service_coordinator import Coordinator

coordinator = Coordinator()


async def chat_loop(message, history):
    resp = ''
    await coordinator.update_last_activity()
    async for chunk in coordinator.user_to_completion(message):
        resp += chunk
        yield resp

def create_gradio_interface():
    # Create the ChatInterface (Gradio v3)
    interface = gr.ChatInterface(
        fn=chat_loop,
        type="messages",
    )
    return interface

async def main_async():
    # Perform any initial startup tasks
    await coordinator.system_start_up()

    # Launch Gradio non-blocking
    interface = create_gradio_interface()
    interface.launch(share=False, prevent_thread_lock=True)
    logging.info("Gradio UI launched in non-blocking mode.")

    # Keep the event loop running
    # This ensures the application stays alive, allowing both Gradio and monitor tasks to run.
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    logging.debug("Starting application...")
    try:
        asyncio.run(main_async())
    except Exception as e:
        logging.error(f"Application encountered an error: {e}")
    logging.debug("Application has exited.")
