import os
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()

class LLMService:
    """
    Service class for interacting with OpenAI's GPT-based language models asynchronously.
    """
    def __init__(self):
        """
        Initialize the LLMService.

        """
        self.model =  os.getenv('GPT_MODEL')
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def send_completion(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        """
        Send a list of messages to the OpenAI API and get a response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with "role" and "content" keys.
            stream (bool): If True, streams the response (currently not implemented).

        Returns:
            str: The assistant's response content.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False  # Temporarily ignoring the stream flag for simplicity
            )
            print(f"API Response: {response}")  # Debug print
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error in send_completion: {e}")
            return "Error: Unable to process the request."

    def summarize_memory(self, memory_content: List[Dict]) -> str:
        """
        Summarize a list of memory objects.

        Args:
            memory_content (List[Dict]): A list of memory objects to summarize.

        Returns:
            str: The summarized memory content.
        """
        prompt = (
            "You will be provided memory objects. Summarize them as concisely as possible while retaining key details."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(memory_content)},
        ]
        print(f"Summarize Memory Input: {messages}")  # Debug print
        return self.send_completion(messages)

    def generate_chat_response(self, chat_log: List[Dict[str, str]]) -> str:
        """
        Generate a response to a user message given a chat log.

        Args:
            chat_log (List[Dict[str, str]]): The chat log containing past messages.

        Returns:
            str: The assistant's response content.
        """
        print(f"Chat Log Input: {chat_log}")  # Debug print
        return self.send_completion(chat_log)

# Example usage
if __name__ == "__main__":
    import asyncio

    def main():
        llm_service = LLMService()

        # Example memory summary
        memory_content = [{"type": "Fact", "content": "The sky is blue."}]
        memory_summary = llm_service.summarize_memory(memory_content)
        print("Memory Summary:", memory_summary)

        # Example chat log
        chat_log = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
        chat_response = llm_service.generate_chat_response(chat_log)
        print("Chat Response:", chat_response)

main()