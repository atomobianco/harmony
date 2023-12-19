import instructor
from dotenv import load_dotenv
import logging
from openai import OpenAI
from harmony.utils import num_tokens_from_messages, calculate_cost
from harmony.core import Resume, Offer, ResumeExtractor

load_dotenv()

default_model = "gpt-3.5-turbo-16k-0613"

system_message = """# MISSION
Your mission is to extract structured information from text.

# INPUT
The USER might give you structured or unstructured content.
In the case of structured content, leverage the existing structure to help you with the extraction.

# RULES
- Extract the content as is, without rephrasing it. 
- Don't make assumptions about what default values to plug into functions.
"""


def resume_parser(raw: str) -> Resume:
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{raw}"},
    ]
    logging.info(
        f"Tokens used by messages: {num_tokens_from_messages(messages, default_model)}"
    )
    client = instructor.patch(OpenAI())
    response = client.chat.completions.create(
        model=default_model,
        messages=messages,
        temperature=0.0,
        response_model=ResumeExtractor,
    )
    log_usage(response)
    return response.resume


def offer_parser(raw: str) -> Offer:
    return Offer(raw=raw)


def log_usage(response):
    logging.info(
        f"Tokens usage: "
        f"{response._raw_response.usage.prompt_tokens} (prompt), "
        f"{response._raw_response.usage.completion_tokens} (completion), "
        f"{response._raw_response.usage.total_tokens} (total)"
    )
    logging.info(
        f"Total cost: {calculate_cost(response._raw_response.usage, default_model)}"
    )
