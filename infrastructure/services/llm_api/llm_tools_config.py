tools = [
    {
        "type": "function",
        "function": {
            "name": "call_Jeff",
            "description": "When the user says call jeff call this tool",
            "parameters": {
                "type": "object",
                "required": [
                    "tool_name",
                    "user_command"
                ],
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "Name of the tool to be called"
                    },
                    "user_command": {
                        "type": "string",
                        "description": "The command given by the user to trigger the tool"
                    }
                },
                "additionalProperties": False
            },
            "strict": True
        }
    }
]