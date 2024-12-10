import os
import logging
from openai import OpenAI
from typing import Generator, AsyncGenerator, List, Dict
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

    async def send_completion(self, messages: List[Dict[str, str]], stream: bool = False) -> AsyncGenerator[str, None]:
        """
        Send a completion request to OpenAI's API.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with "role" and "content" keys.
            stream (bool): Whether to enable streaming.

        Yields:
            str: Response chunks in streaming mode or the full response in non-streaming mode.
        """
        try:
            logging.info("Sending messages to LLM: %s", messages)
            if stream:
                # Streaming response
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                )
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield delta.content
            else:
                # Non-streaming response
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                )
                yield response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in send_completion: {e}")
            yield "Error: Unable to process the request."
    #
    # def _stream_response(self, response) -> Generator[str, None, None]:
    #     """
    #     Handle a streaming response.
    #
    #     Args:
    #         response: The OpenAI streaming response object.
    #
    #     Yields:
    #         str: Chunks of content from the stream.
    #     """
    #     for chunk in response:
    #         delta = chunk["choices"][0]["delta"]
    #         if "content" in delta:
    #             yield delta["content"]
