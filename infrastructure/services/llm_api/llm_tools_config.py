tools=[
    {
      "type": "function",
      "function": {
        "name": "rank_complexity",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "request",
            "complexity_level"
          ],
          "properties": {
            "request": {
              "type": "string",
              "description": "The question or request to be ranked"
            },
            "complexity_level": {
              "enum": [
                "low",
                "medium",
                "high",
                "extreme"
              ],
              "type": "string",
              "description": "The complexity ranking of the request"
            }
          },
          "additionalProperties": False
        },
        "description": "Rank a question or request in complexity: low, medium, high, extreme"
      }
    },
    {
      "type": "function",
      "function": {
        "name": "provide_steps_for_complex_question",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "complexity_level",
            "question",
            "context",
            "steps"
          ],
          "properties": {
            "steps": {
              "type": "array",
              "items": {
                "type": "string",
                "description": "A specific step or consideration needed to solve the question."
              },
              "description": "List of steps or considerations to address the complex question."
            },
            "context": {
              "type": "string",
              "description": "Additional context or background information relevant to the question."
            },
            "question": {
              "type": "string",
              "description": "The question that requires a structured response for solving."
            },
            "complexity_level": {
              "type": "string",
              "description": "The level of complexity of the question, should be either 'high' or 'extreme'."
            }
          },
          "additionalProperties": False
        },
        "description": "If given a high or extreme complexity question, provide a list of steps or considerations needed to solve the provided question. If a choice is needed, provide options or recomendations."
      }
    }
  ]