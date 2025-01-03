tools = [
    {
        "type": "function",
        "function": {
            "name": "add_remember_item",
            "description": "adds an item to the remember list. Use if need to recall something for the user or for any information that seems especially important to you to recall. Also use this if you learn something about your user or yourself that you find novel",
            "parameters": {
                "type": "object",
                "required": [
                    "item_name",
                    "item_details",
                    "tags"
                ],
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to remember"
                    },
                    "item_details": {
                        "type": "string",
                        "description": "Additional details or context about the item"
                    },
                    "tags": {
                        "type": "array",
                        "description": "Optional tags for categorizing the item",
                        "items": {
                            "type": "string",
                            "description": "A tag for the item"
                        }
                    }
                },
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_remember_list",
            "description": "If you need to recall an item from the list of recently stored memories. Returns a list.",
            "parameters": {
                "type": "object",
                "required": [
                    "limit",
                    "filter"
                ],
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of memories to recall"
                    },
                    "filter": {
                        "type": "string",
                        "description": "Criteria to filter the memories"
                    }
                },
                "additionalProperties": False
            },
            "strict": True
        }
    }
]