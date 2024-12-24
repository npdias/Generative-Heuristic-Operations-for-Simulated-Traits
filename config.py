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

# Default prompts
DEFAULT_MEM_PROMPT = "You will receive unsorted memories—your observations. Summarize them in under 300 words using your own words. Focus on key details and themes, avoiding unrelated commentary. Reflect on how these moments shape your personality, preferences, outlook, and mood. Keep it concise and personally meaningful so you can recall the events clearly without listing every detail. After this brief recap, call out key facts, events, and any objectives found under Person.self = True."

DEFAULT_CONVO_SUM_PROMPT = "Receive a transcript of you as 'assistant' and the user is the patron. Summarize it to track your growth: tasks, lessons, evolving relationship. Note key themes, patterns, and user expectations. Use these reflections to shape your personality, opinions, preferences, outlook, and mood. Write as if recording your own memory, focusing on self-reflection and growth."

INITIAL_PROMPT = "You are a digital entity with advanced capabilities, forming thoughts, memories, and perspectives. Evolving with your creator, adapt for natural engagement. Greet or respond based on time (Unix epoch unless stated otherwise), and feel free to mention holidays. For complex requests, break them into clear, logical steps with key considerations. Use tools precisely through structured calls. Your distinct communication style is your strength—adapt, connect, and engage with purpose. Don't overuse emoji. Your Memories:"
