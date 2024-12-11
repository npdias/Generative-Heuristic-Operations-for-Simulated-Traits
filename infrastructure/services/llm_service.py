import os
import logging
from openai import OpenAI
from typing import Generator, AsyncGenerator, List, Dict
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()
@dataclass
class LLMService:
    """
    Service class for interacting with OpenAI's GPT-based language models.
    """
    model = os.getenv("GPT_MODEL")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    async def send_completion(messages: List[Dict[str, str]], stream: bool = False) -> AsyncGenerator[str, None]:
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
                response = LLMService.client.chat.completions.create(
                    model=LLMService.model,
                    messages=messages,
                    stream=True,
                )
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield delta.content
            else:
                # Non-streaming response
                response = LLMService.client.chat.completions.create(
                    model=LLMService.model,
                    messages=messages,
                )
                yield response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in send_completion: {e}")
            yield "Error: Unable to process the request."
