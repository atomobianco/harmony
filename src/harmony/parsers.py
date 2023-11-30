import json
from dotenv import load_dotenv
import logging
from openai import OpenAI
import os
from dacite import from_dict
from harmony.utils import num_tokens_from_messages, calculate_cost
from harmony.core import Position, Resume, Offer

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model_name = "gpt-3.5-turbo-16k-0613"

# TODO = reduce hallucinations
#  - https://www.youtube.com/watch?v=1yOxOo84yqU
#  - > 3.5 is very bad at negative prompts, like “we don’t have x” or “do NOT return an answer if you’re unsure” … you have to phrase things in positive instructions. Gpt-4 is much, much better at handling negatives (OpenAI calls this out on their model card).
#    https://community.openai.com/t/building-hallucination-resistant-prompts/131036/26?page=2

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
                        "job_title": {
                            "type": "string",
                            "description": "The official title held at the company, e.g. Software Engineer",
                        },
                        "company_name": {
                            "type": "string",
                            "description": "The name of the company or organization where one worked, e.g. Google",
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date for the position, e.g. 2019",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date for the position, e.g. 2019",
                        },
                        "company_location": {
                            "type": "string",
                            "description": "The city and country where the company is located, e.g. Paris, France",
                        },
                        "tasks": {
                            "type": "array",
                            "description": "Responsibilities or achievements accomplished in this position",
                            "items": {
                                "type": "string",
                                "description": "The responsibility or achievement accomplished in this position",
                            },
                        },
                        "skills": {
                            "type": "array",
                            "description": "Skills utilized or gained during this job",
                            "items": {
                                "type": "string",
                                "description": "Skill utilized or gained during this job",
                            },
                        },
                        "tools": {
                            "type": "array",
                            "description": "Tools, software, or programming languages used in this role",
                            "items": {
                                "type": "string",
                                "description": "Tool, software, or programming language used in this role",
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
                    "skills": {
                        "type": "array",
                        "description": "Skills utilized or gained during this job",
                        "items": {
                            "type": "string",
                            "description": "A list of skills",
                        },
                    },
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
        {"role": "user", "content": f"```{raw}```"},
    ]
    logging.info(f"Tokens messages: {num_tokens_from_messages(messages, model_name)}")
    functions = [parse_positions_function]
    response = client.chat.completions.create(
        model=model_name, messages=messages, functions=functions, function_call="auto"
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
        positions = function_args.get("positions", [])
    else:
        positions = []
    return [from_dict(data_class=Position, data=p) for p in positions]


def resume_parser(raw: str) -> Resume:
    """Parse a resume and return structured data."""
    messages = [
        {"role": "user", "content": f"```{raw}```"},
    ]
    logging.info(
        f"Tokens used by messages: {num_tokens_from_messages(messages, model_name)}"
    )
    functions = [parse_resume_function]
    response = client.chat.completions.create(
        model=model_name, messages=messages, functions=functions, function_call="auto"
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
        try:
            function_args = json.loads(response_message["function_call"]["arguments"])
        except json.decoder.JSONDecodeError:
            logging.error(f"Error parsing function call: {response_message}")
            raise
        else:
            resume = function_args.get("resume", {})
    else:
        resume = {}
    summary = resume.get("summary", "")
    skills = resume.get("skills", "")
    positions = [
        from_dict(data_class=Position, data=p) for p in resume.get("positions", [])
    ]
    return Resume(raw=raw, summary=summary, skills=skills, positions=positions)


def offer_parser(raw: str) -> Offer:
    return Offer(raw=raw)
