"""
conversation.py

"""

from dataclasses import dataclass, field
from infrastructure.models.memory import Memory

@dataclass(kw_only=True)
class Conversation(Memory):
    """
    Represents a conversation memory with a transcript and summary.

    Attributes:
        mem_type (str): Specifies the type of memory, default is 'Conversation'.
        transcript (str): The full transcript of the conversation.
        summary (str): A brief summary of the conversation's key details.
    """
    transcript: str
    summary: str = ""
    mem_type: str = field(default="Conversation")

    def __str__(self):
        """
        Returns a formatted string representation of the conversation.

        Returns:
            str: A string showing the transcript and summary.
        """
        return f"[{self.mem_type}] Transcript: {self.transcript}\nSummary: {self.summary}"
