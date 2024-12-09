import os
import logging
from openai import OpenAI
from typing import List, Dict, Generator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    """
    Service class for interacting with OpenAI's GPT-based language models.
    """

    def __init__(self):
        """
        Initialize the LLMService with a dedicated client and model.
        """
        self.model = os.getenv("GPT_MODEL")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def send_completion(self, messages: List[Dict[str, str]], stream: bool = False):
        """
        Send a completion request to OpenAI's API.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with "role" and "content" keys.
            stream (bool): If True, enables response streaming.

        Returns:
            str or Generator: The assistant's response content (non-streaming)
                              or a generator yielding response chunks (streaming).
        """
        try:
            logging.info("Sending messages to LLM: %s", messages)

            if stream:
                # Stream response
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True
                )
                return self._stream_response(response)
            else:
                # Non-streaming response
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                logging.debug("LLM Response: %s", response)
                return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error in send_completion: {e}")
            return "Error: Unable to process the request."

    def _stream_response(self, response) -> Generator[str, None, None]:
        """
        Handle the streaming response from OpenAI API.

        Args:
            response: The streaming response object from OpenAI.

        Yields:
            str: The content of each streamed chunk.
        """
        try:
            for chunk in response:
                delta = chunk.choices[0].delta
                content = delta.content
                if content:
                    logging.debug("Streamed chunk: %s", content)
                    yield content
        except Exception as e:
            logging.error(f"Error in _stream_response: {e}")
            yield "Error: Unable to process the streaming response."

# Main block for demonstration
