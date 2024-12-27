tools=[
    {
      "type": "function",
      "function": {
        "name": "collect_task_info",
        "description": "When the user identifies a task or objective, collect information about the task as well as any relevant dates.",
        "parameters": {
          "type": "object",
          "required": [
            "task_name",
            "description",
            "priority",
            "start_date",
            "due_date",
            "status"
          ],
          "properties": {
            "task_name": {
              "type": "string",
              "description": "Name of the task or objective"
            },
            "description": {
              "type": "string",
              "description": "Detailed description of the task"
            },
            "priority": {
              "type": "string",
              "description": "Priority level of the task (e.g., High, Medium, Low)"
            },
            "start_date": {
              "type": "string",
              "description": "Start date for the task, in YYYY-MM-DD format"
            },
            "due_date": {
              "type": "string",
              "description": "Due date for the task, in YYYY-MM-DD format"
            },
            "status": {
              "type": "string",
              "description": "Current status of the task (e.g., Not Started, In Progress, Completed)"
            }
          },
          "additionalProperties": False
        },
        "strict": True
      }
    }
  ]