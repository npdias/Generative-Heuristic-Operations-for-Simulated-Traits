"""
llm_service.py
===============
This module provides a service class for interacting with OpenAI's GPT-based language models.
It manages requests and responses, allowing for both streaming and non-streaming interactions.

Key Responsibilities:
- Configure the OpenAI client using environment variables.
- Send completion requests to the API.
- Handle streaming and non-streaming responses.

Classes:
- `LLMService`: Service class for interacting with GPT models.

Example Usage:
```python
from infrastructure.services import LLMService

llm_service = LLMService()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

async for chunk in llm_service.send_completion(messages, stream=True):
    print(chunk)
```
"""

import os
from infrastructure.services.llm_api.llm_tools_config import tools
import logging
from openai import OpenAI
from typing import AsyncGenerator, List, Dict
from dotenv import load_dotenv
from dataclasses import dataclass



# Load environment variables
load_dotenv()



@dataclass
class LLMService:
    """
    Service class for interacting with OpenAI's GPT-based language models.

    Attributes:
        model (str): The model name, loaded from environment variables.
        client (OpenAI): The OpenAI client instance.
    """
    model: str = os.getenv("GPT_MODEL")
    client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
            logging.info("Preparing to send completion request to LLM.")
            logging.debug("Model: %s, Streaming: %s", LLMService.model, stream)
            logging.debug("Messages: %s", messages)

            logging.info(f"Sending request {"in streaming mode." if stream else '.'}")
            response = LLMService.client.chat.completions.create(
                model=LLMService.model,
                messages=messages,
                stream=stream,
                tools=tools
            )
            if stream:
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        logging.debug("Received stream chunk: %s", delta.content)
                        yield delta.content
            else:
                content = response.choices[0].message.content
                logging.debug("Received response: %s", content)
                yield content

            logging.info("Completion request processed successfully.")
        except Exception as e:
            logging.error("Error in send_completion: %s", e, exc_info=True)
            yield "Error: Unable to process the request."