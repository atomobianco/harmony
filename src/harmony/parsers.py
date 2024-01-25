import instructor
from dotenv import load_dotenv
import logging
from openai import OpenAI
from harmony.utils import num_tokens_from_messages, log_usage
from harmony.core import Resume, Offer, ResumeExtractor
from pkg_resources import resource_stream

load_dotenv()

default_model = "gpt-3.5-turbo-16k-0613"

sys_msg = resource_stream(__name__, "system/resume_parser.md").read().decode("utf-8")


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
        response_model=ResumeExtractor,
    )
    log_usage(response, default_model)
    return response.resume


def offer_parser(raw: str) -> Offer:
    return Offer(raw=raw)
