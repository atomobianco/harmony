from dotenv import load_dotenv
from harmony.core import Resume, Offer
from openai import OpenAI
import os
from pkg_resources import resource_stream

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

default_model = "gpt-4-1106-preview"

cover_letter_system_message = (
    resource_stream(__name__, "system/cover_letter_writer.md").read().decode("utf-8")
)

strengths_weaknesses_system_message = (
    resource_stream(__name__, "system/strengths_weaknesses_writer.md")
    .read()
    .decode("utf-8")
)


def cover_letter_writer(resume: str, offer: str) -> str:
    sys_message = cover_letter_system_message
    user_message = f"<resume>\n{resume}\n</resume>\n\n<offer>{offer}</offer>"
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": user_message},
    ]
    response = client.chat.completions.create(model=default_model, messages=messages)
    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


def strengths_weaknesses_writer(resume: str, offer: str) -> str:
    sys_message = strengths_weaknesses_system_message
    user_message = f"# RESUME\n\n{resume}\n\n# OFFER\n\n{offer}"
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": user_message},
    ]
    response = client.chat.completions.create(model=default_model, messages=messages)
    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result
