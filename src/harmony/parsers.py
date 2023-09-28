import json
from dotenv import load_dotenv
import logging
import openai
import os
import pyaml


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

system_message = "You are a recruiter. You have a resume and want to parse it."
system_message = (
    "You are a recruiter. Your role is to take a resume detailed by tripel back  ticks and return a "
    "structured response as defined by the functions detailed"
)

parse_summary_function = {
    "name": "parse_summary",
    "description": "Get the candidate's summary from a resume",
    "parameters": {
        "type": "object",
        "require": "summary",
        "properties": {
            "summary": {
                "type": "string",
                "description": "The summary of the candidate",
            },
        },
    },
}

parse_positions_function = {
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

parse_resume_function = {
    "name": "parse_resume",
    "description": "Get the candidate's summary and positions from a resume",
    "parameters": {
        "type": "object",
        "properties": {
            "resume": {
                "type": "object",
                "properties": {
                    "summary": parse_summary_function["parameters"]["properties"][
                        "summary"
                    ],
                    "positions": parse_positions_function["parameters"]["properties"][
                        "positions"
                    ],
                },
            },
        },
    },
}


def positions_parser(raw: str) -> list[dict]:
    """Parse a resume and return a list of positions."""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"```{raw}```"},
    ]
    functions = [parse_positions_function]
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
    logging.info(f"positions:\n{pyaml.dump(result)}")
    return result


def resume_parser(raw: str) -> dict:
    """Parse a resume and return structured data."""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"```{raw}```"},
    ]
    functions = [parse_resume_function]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        resume = function_args.get("resume")
        result = resume
    else:
        result = {}
    logging.info(f"resume:\n{pyaml.dump(result)}")
    return result
