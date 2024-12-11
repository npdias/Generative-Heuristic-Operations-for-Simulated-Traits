from dataclasses import dataclass
from infrastructure.models import Memory
from infrastructure.services.llm_service import LLMService
import logging


@dataclass
class Conversation(Memory):
    transcript: str
    summary: str = ""  # Default value for summary

    def __post_init__(self):
        self.mem_type = "Conversation"
        super().__post_init__()  # Add to Memory.all_memories

    @classmethod
    async def create(cls, transcript: str):
        """
        Asynchronous factory method to create a Conversation instance.

        Args:
            transcript (str): The transcript of the conversation.

        Returns:
            Conversation: A new Conversation instance with a generated summary.
        """
        try:
            llm_service = LLMService()
            messages = [
                {"role": "system", "content": "You are a summarization assistant."},
                {"role": "user", "content": f"Summarize this conversation:\n\n{transcript}"}
            ]
            # Collect all chunks from the async generator
            summary_chunks = []
            async for chunk in llm_service.send_completion(messages, stream=False):
                summary_chunks.append(chunk)
            summary = "".join(summary_chunks)  # Combine all chunks into a single string
        except Exception as e:
            logging.error(f"Failed to generate summary: {e}")
            summary = "Error: Unable to generate summary."

        # Create the Conversation instance
        return cls(transcript=transcript, summary=summary)

# # Example usage
if __name__ == "__main__":
    import asyncio
    from infrastructure.models import Conversation


    async def main():
        # Create a new conversation asynchronously
        convo = await Conversation.create(transcript="User: Hi! How are you?\nAssistant: I'm fine, thank you.")

        print("Transcript:", convo.transcript)
        print("Summary:", convo.summary)
        print("Memory Type:", convo.mem_type)


    asyncio.run(main())