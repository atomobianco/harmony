from dotenv import load_dotenv
from harmony.core import Resume
from openai import OpenAI
import os
from harmony.utils import read_sys_msg

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
default_model = "gpt-4-1106-preview"

cover_letter_system_message = read_sys_msg("cover_letter_writer.md")
strengths_weaknesses_system_message = read_sys_msg("strengths_weaknesses_writer.md")


def cover_letter_writer(resume: str | Resume, offer: str) -> str:
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


def strengths_weaknesses_writer(resume: str | Resume, offer: str) -> str:
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
