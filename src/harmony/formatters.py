from harmony.core import Resume, Position, Offer
from openai import OpenAI
from dotenv import load_dotenv
import os
import copy
import logging
from harmony.utils import num_tokens_from_messages, log_usage
from pkg_resources import resource_stream

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

default_model = "gpt-4-1106-preview"

sys_msg_position = (
    resource_stream(__name__, "system/position_formatter.md").read().decode("utf-8")
)

sys_msg_position_aligned = (
    resource_stream(__name__, "system/position_aligned_formatter.md")
    .read()
    .decode("utf-8")
)

sys_msg_skills = (
    resource_stream(__name__, "system/skills_formatter.md").read().decode("utf-8")
)


def position_formatter(position: Position | str, offer: Offer | str = None) -> str:
    position_str = str(position)
    sys_msg = sys_msg_position_aligned if offer else sys_msg_position
    user_msg = (
        f"<position>\n{position_str}\n<position>\n\n<offer>\n{offer}\n</offer>"
        if offer
        else position_str
    )
    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": user_msg},
    ]
    logging.info(
        f"Tokens messages: {num_tokens_from_messages(messages, default_model)}"
    )
    response = client.chat.completions.create(
        model=default_model,
        messages=messages,
        temperature=0.0,
        # Set the temperature to a lower value, such as 0.2, to make the output more deterministic and focused.
        # This will help ensure that the generated text is concise and less prone to randomness.
        top_p=0.8,
        # Use a moderate value for Top P, such as 0.8. This will allow the model to select from a reasonably broad
        # range of tokens while still maintaining control over the generated text.
        frequency_penalty=0.8,
        # Increase the frequency penalty to discourage the repetition of words or phrases. A value around 0.5 or
        # higher can help reduce redundancy in the generated content.
        presence_penalty=0.8,
        # Similarly, you can increase the presence penalty to discourage the inclusion of similar words or phrases.
        # A value around 0.5 or higher can encourage the model to provide more varied rephrasing.
    )
    log_usage(response, default_model)

    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


def skills_formatter(skills: str, model: str = "gpt-3.5-turbo-0613") -> str:
    messages = [
        {"role": "system", "content": sys_msg_skills},
        {"role": "user", "content": skills},
    ]
    logging.info(
        f"Tokens messages: {num_tokens_from_messages(messages, default_model)}"
    )
    response = client.chat.completions.create(model=model, messages=messages)
    log_usage(response, model)

    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


def resume_formatter(resume: Resume, offer: Offer = None) -> str:
    resume_copy = copy.deepcopy(resume)

    # Rework the positions one by one
    resume_copy.experience = [
        position_formatter(pos, offer) for pos in resume.experience
    ]

    # Rework the skills
    all_skills = resume.skills + [
        skill for position in resume.experience for skill in position.skills
    ]
    resume_copy.skills = [
        skill.strip() for skill in skills_formatter(", ".join(all_skills)).split(",")
    ]

    return str(resume_copy)
