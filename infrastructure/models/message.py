from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import time


class Content(BaseModel):
    type: str = Field(default="text", description="Type of content, e.g. 'text'")
    text: str = Field(..., description="Text content")


class ToolFunction(BaseModel):
    name: str = Field(..., description="name of function passed by tool_call")
    arguments: str = Field(..., description="character escaped string of arguments")


class ToolCall(BaseModel):
    id: str = Field(..., description="ID of tool_call event - user by openAi for tracking responses")
    type: str =Field(default='function', description="Type of content, e.g. 'text'")
    function: Optional[ToolFunction] = Field(default=None,
                                        description="Tool Function object if the message is from a tool")


class Message(BaseModel):
    role: Literal['user', 'assistant', 'tool', 'system'] = Field(..., description="The role of the message (user, assistant, tool, system)")
    timestamp: float = Field(default_factory=time.time)


    content: Optional[List[Content]] = Field(kw_only=True, default=None, description="List of content items")

    tool_calls: Optional[List[ToolCall]] = Field(kw_only=True, default=None, description="List of tool call items")

    # For the tool_call_id, mark it optional (because not all messages have it)
    tool_call_id: Optional[str] = Field(kw_only=True, default=None, description="Reference to a tool call ID if the message is from a tool")
