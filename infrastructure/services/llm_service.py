import openai
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict

# Load environment variables from .env file
load_dotenv()

class LLMService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided or missing in environment variables.")
        openai.api_key = self.api_key

    async def send_completion(self, messages: List[Dict[str, str]], model: str = "gpt-4", stream: bool = False) -> Optional[str]:
        """
        Send a completion request to the LLM API.

        Args:
            messages (List[Dict[str, str]]): List of message dicts (e.g., {"role": "user", "content": "Hi"}).
            model (str): The LLM model to use (default: "gpt-4").
            stream (bool): If True, enable chunked responses.

        Returns:
            Optional[str]: The LLM response or None in case of an error.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=stream
            )

            if stream:
                return self._handle_stream(response)
            else:
                return response.choices[0].message.content
        except Exception as e:
            print(f"Error in send_completion: {e}")
            return None

    def _handle_stream(self, response) -> str:
        """Handle streaming responses from the LLM."""
        try:
            result = ""
            for chunk in response:
                if chunk.get("choices"):
                    delta = chunk["choices"][0]["delta"]
                    if "content" in delta:
                        result += delta["content"]
            return result
        except Exception as e:
            print(f"Error in _handle_stream: {e}")
            return ""

    async def summarize_memory(self, memory_content: List[Dict[str, str]]) -> Optional[str]:
        """
        Summarize memory content using the LLM.

        Args:
            memory_content (List[Dict[str, str]]): List of memory objects to summarize.

        Returns:
            Optional[str]: The summary or None in case of an error.
        """
        instructions = (
            "You will be provided memory objects. Summarize them as concisely as possible while retaining key details."
        )
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": str(memory_content)},
        ]
        return await self.send_completion(messages)

    async def generate_chat_response(self, chat_log: List[Dict[str, str]]) -> Optional[str]:
        """
        Generate a response for a chat log using the LLM.

        Args:
            chat_log (List[Dict[str, str]]): List of chat messages.

        Returns:
            Optional[str]: The generated response or None in case of an error.
        """
        return await self.send_completion(chat_log)
