"""
conversation.py
===============
This module defines the `Conversation` class, a specialized type of memory for
storing and managing conversational data. Conversations include both a transcript
and a summary to encapsulate key details and themes.

Key Responsibilities:
- Represent conversational memories with transcript and summary fields.
- Provide a clear textual representation of the conversation.

Classes:
- `Conversation`: Memory subclass for conversational data.

Example Usage:
```python
from infrastructure.models.conversation import Conversation

conversation = Conversation(
    transcript="User: Hi\nAssistant: Hello!",
    summary="A friendly greeting between the user and assistant."
)
print(conversation)
```
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
    mem_type: str = field(default="Conversation")
    transcript: str
    summary: str = ""

    def __str__(self):
        """
        Returns a formatted string representation of the conversation.

        Returns:
            str: A string showing the transcript and summary.
        """
        return f"[{self.mem_type}] Transcript: {self.transcript}\nSummary: {self.summary}"
