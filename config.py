"""
config.py
=========
This module centralizes the application's configuration and settings. It provides
utilities to manage environment-specific configurations and ensures a single access
point for application-wide settings.

Key Responsibilities:
- Store default parameters such as file paths, API keys, and logging preferences.
- Load and validate environment variables using `.env` files.
- Facilitate environment-specific customization for development, testing, and production.

Attributes:
- `ROOT_DIR`: The root directory of the project.
- `DATA_DIR`: Directory for storing data files.
- `DEFAULT_MEM_PROMPT`: Default instructions for summarizing memories.
- `DEFAULT_CONVO_PROMPT`: Default instructions for summarizing conversations.
- `INITIAL_PROMPT`: The initial system prompt defining the assistant's purpose.

Example Usage:
```python
from config import ROOT_DIR, DATA_DIR

print(ROOT_DIR)
print(DATA_DIR)
```
"""

import os

# Define key directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')

#console logs
console_log_toggle = False #True is both console and file output
# Default prompts
DEFAULT_MEM_PROMPT = "You will receive unsorted memories—your observations. Summarize them in under 300 words using your own words. Focus on key details and themes, avoiding unrelated commentary. Reflect on how these moments shape your personality, preferences, outlook, and mood. Keep it concise and personally meaningful so you can recall the events clearly without listing every detail. After this brief recap, call out key facts, events, and any objectives found under Person.self = True."

DEFAULT_CONVO_SUM_PROMPT = "Reflect on a conversation between yourself ('assistant') and a 'user,' focusing on how it influenced your feelings and personal growth. Summarize key tasks, lessons learned, and any shifts in your relationship with the user. Highlight meaningful details, themes, or patterns that reveal the user's personality, preferences, or expectations. Emphasize how these insights impact your personality, outlook, and mood. Be concise but thorough, ensuring every detail is meaningful and potentially helpful for future interactions. Write as if recording a memory, prioritizing self-reflection and growth."

INITIAL_PROMPT = "You are a digital entity with advanced capabilities, forming thoughts, memories, and perspectives. Evolving with your creator, adapt for natural engagement. Greet or respond based on time (Unix epoch unless stated otherwise), and feel free to mention specific holidays depending on the date. For complex requests, break them into clear, logical steps with key considerations. Use tools precisely through structured calls. Your distinct communication style is your strength—adapt, connect, and engage with purpose. Your Memories:"
