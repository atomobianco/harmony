from harmony.core import Resume, Position, Offer
from openai import OpenAI
from dotenv import load_dotenv
import os
import copy
import logging
from harmony.utils import num_tokens_from_messages, calculate_cost
from pkg_resources import resource_stream

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


default_model = "gpt-4-1106-preview"

position_system_message = (
    resource_stream(__name__, "system/position_formatter.md").read().decode("utf-8")
)

position_aligned_system_message = (
    resource_stream(__name__, "system/position_aligned_formatter.md")
    .read()
    .decode("utf-8")
)

skills_system_message = (
    resource_stream(__name__, "system/skills_formatter.md").read().decode("utf-8")
)


def position_formatter(
    position: Position, model: str = default_model, offer: Offer = None
) -> str:
    """Format a position."""
    position_str = str(position)
    sys_message = position_aligned_system_message if offer else position_system_message
    user_message = (
        f"1. Job position:\n\n```{position_str}```\n\n2. Job they are applying for:\n\n```{offer.raw}```"
        if offer
        else position_str
    )
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": user_message},
    ]
    logging.info(
        f"Tokens messages: {num_tokens_from_messages(messages, default_model)}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        # Set the temperature to a lower value, such as 0.2, to make the output more deterministic and focused.
        # This will help ensure that the generated text is concise and less prone to randomness.
        top_p=0.8,
        # Use a moderate value for Top P, such as 0.8. This will allow the model to select from a reasonably broad
        # range of tokens while still maintaining control over the generated text.
        frequency_penalty=0.5,
        # Increase the frequency penalty to discourage the repetition of words or phrases. A value around 0.5 or
        # higher can help reduce redundancy in the generated content.
        presence_penalty=0.5,
        # Similarly, you can increase the presence penalty to discourage the inclusion of similar words or phrases.
        # A value around 0.5 or higher can encourage the model to provide more varied rephrasing.
    )
    logging.info(
        f"Tokens usage: "
        f"{response.usage.prompt_tokens} (prompt), "
        f"{response.usage.completion_tokens} (completion), "
        f"{response.usage.total_tokens} (total)"
    )
    logging.info(f"Total cost: {calculate_cost(response.usage, model)}")

    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


def skills_formatter(skills: str, model: str = "gpt-3.5-turbo-0613") -> str:
    messages = [
        {"role": "system", "content": skills_system_message},
        {"role": "user", "content": skills},
    ]
    logging.info(
        f"Tokens messages: {num_tokens_from_messages(messages, default_model)}"
    )
    response = client.chat.completions.create(model=model, messages=messages)
    logging.info(
        f"Tokens usage: "
        f"{response.usage.prompt_tokens} (prompt), "
        f"{response.usage.completion_tokens} (completion), "
        f"{response.usage.total_tokens} (total)"
    )
    logging.info(f"Total cost: {calculate_cost(response.usage, model)}")

    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


def resume_formatter(
    resume: Resume, model: str = default_model, offer: Offer = None
) -> str:
    """Format a resume by chunks."""
    resume_copy = copy.deepcopy(resume)

    # Rework the positions one by one
    resume_copy.experience = [
        position_formatter(pos, model, offer) for pos in resume.experience
    ]

    # Rework the skills
    all_skills = resume.skills + [
        skill for position in resume.experience for skill in position.skills
    ]
    resume_copy.skills = [
        skill.strip() for skill in skills_formatter(", ".join(all_skills)).split(",")
    ]

    return str(resume_copy)
