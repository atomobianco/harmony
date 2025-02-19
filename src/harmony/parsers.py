import instructor
from dotenv import load_dotenv
import logging
from openai import OpenAI
from harmony.utils import num_tokens_from_messages, log_usage, read_sys_msg
from harmony.core import Resume, Offer

load_dotenv()

default_model = "gpt-3.5-turbo-16k-0613"

sys_msg = read_sys_msg("resume_parser.md")


def resume_parser(raw: str) -> Resume:
    messages = [
        {"role": "system", "content": sys_msg},
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
        response_model=Resume,
    )
    log_usage(response, default_model)
    return response


def offer_parser(raw: str) -> Offer:
    return Offer(raw=raw)
