import json
from dotenv import load_dotenv
import logging
import openai
import os
from dacite import from_dict
from harmony.utils import num_tokens_from_messages, calculate_cost
from harmony.core import Position, Resume

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

model_name = "gpt-3.5-turbo-16k"

# TODO = reduce hallucinations
#  - https://www.youtube.com/watch?v=1yOxOo84yqU
#  - > 3.5 is very bad at negative prompts, like “we don’t have x” or “do NOT return an answer if you’re unsure” … you have to phrase things in positive instructions. Gpt-4 is much, much better at handling negatives (OpenAI calls this out on their model card).
#    https://community.openai.com/t/building-hallucination-resistant-prompts/131036/26?page=2

system_message = "You are a recruiter. You have a resume and want to parse it."
system_message = (
    "You are a recruiter. Your role is to take a resume detailed by triple back ticks and return a "
    "structured response as defined by the functions detailed."
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
                        "role": {
                            "type": "string",
                            "description": "The role of the position (e.g. Software Engineer)",
                        },
                        "company": {
                            "type": "string",
                            "description": "The company of position (e.g. Google)",
                        },
                        "start": {
                            "type": "string",
                            "description": "The start date of position",
                        },
                        "end": {
                            "type": "string",
                            "description": "The end date of position",
                        },
                        "location": {
                            "type": "string",
                            "description": "The location of position",
                        },
                        "tasks": {
                            "type": "array",
                            "description": "The responsibilities or accomplishments of position",
                            "items": {
                                "type": "string",
                                "description": "A responsibility or accomplishment of position",
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


def positions_parser(raw: str) -> list[Position]:
    """Parse a resume and return a list of positions."""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"```{raw}```"},
    ]
    logging.info(f"Tokens messages: {num_tokens_from_messages(messages, model_name)}")
    functions = [parse_positions_function]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    logging.info(
        f"Tokens usage: "
        f"{response.usage.prompt_tokens} (prompt), "
        f"{response.usage.completion_tokens} (completion), "
        f"{response.usage.total_tokens} (total)"
    )
    logging.info(f"Total cost: {calculate_cost(response.usage)}")

    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        positions = function_args.get("positions")
        result = positions
    else:
        result = []
    positions = [from_dict(data_class=Position, data=p) for p in result]
    return positions


def resume_parser(raw: str) -> Resume:
    """Parse a resume and return structured data."""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"```{raw}```"},
    ]
    logging.info(
        f"Tokens used by messages: {num_tokens_from_messages(messages, model_name)}"
    )
    functions = [parse_resume_function]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    logging.info(
        f"Tokens usage: "
        f"{response.usage.prompt_tokens} (prompt), "
        f"{response.usage.completion_tokens} (completion), "
        f"{response.usage.total_tokens} (total)"
    )
    logging.info(f"Total cost: {calculate_cost(response.usage)}")

    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        resume = function_args.get("resume")
        result = resume
    else:
        result = {}
    summary = result["summary"]
    positions = [from_dict(data_class=Position, data=p) for p in resume["positions"]]
    return Resume(raw=raw, summary=summary, positions=positions)
