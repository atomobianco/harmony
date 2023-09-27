import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def positions_parser(raw: str) -> list[dict]:
    """Parse a resume and return a list of positions."""
    messages = [{"role": "user", "content": raw}]
    functions = [
        {
            "name": "parse_positions",
            "description": "Get the candidate's positions from a resume",
            "parameters": {
                "type": "object",
                "properties": {
                    "positions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "The title of the position",
                                },
                                "start": {
                                    "type": "string",
                                    "description": "The start date of position (2023 if not a date)",
                                },
                                "end": {
                                    "type": "string",
                                    "description": "The end date of position (2023 if not a date)",
                                },
                                "location": {
                                    "type": "string",
                                    "description": "The location of the position",
                                },
                                "tasks": {
                                    "type": "array",
                                    "description": "The responsibilities or accomplishments of position",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "description": {
                                                "type": "string",
                                                "description": "The description of the task",
                                            }
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        positions = function_args.get("positions")
        result = positions
    else:
        result = []
    return result
