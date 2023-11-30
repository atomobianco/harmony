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


default_model = "gpt-4-0613"

system_message = (
    "Ignore all previous instructions. "
    "From this point forward, you are a professional recruiter with years of experience analysing and improving "
    "Curriculum Vitae (CV) and resumes."
)

position_system_message = (
    resource_stream(__name__, "data/position_system_message.md").read().decode("utf-8")
)

position_aligned_system_message = (
    resource_stream(__name__, "data/position_aligned_system_message.md")
    .read()
    .decode("utf-8")
)

skills_system_message = (
    resource_stream(__name__, "data/skills_system_message.md").read().decode("utf-8")
)

intro_position_message = (
    "Here follows, surrounded by triple back ticks, a position that a candidate held, along with a list of tasks that "
    "the candidate was responsible and accomplished during the job."
)

intro_tasks_message = (
    "Here follows, surrounded by triple back ticks, a list of tasks that a candidate was responsible and accomplished "
    "during the job."
)

intro_resume_message = (
    "Here follows, surrounded by triple back ticks, a resume of a candidate."
)

intro_offer_message = (
    "Here follows, surrounded by triple back ticks, an offer of a job position."
)

outro_tasks_message_1 = (
    "Your task is to improve the candidate's resume."
    "Create a shorter list (approximately 8 items) that resume this candidate's major contributions."
    "Each list item should be concise and be no longer than 20 words."
    "Keep this list diverse, and avoid repeating similar tasks."
    "Avoid specifying the names of programming languages, tools, or cloud environments."
)

outro_tasks_message_2 = (
    "Your task is to improve the candidate's resume so that it aligns with the job offer."
    "First, separate the list of responsibilities and accomplishments of the candidate into two groups."
    "In the first group, put all that concerns with technical leadership."
    "In the second group, put all that concerns with management leadership."
    "Then, condense the two groups to have no more than 10 items each."
    "Do so by rephrasing and merging together items which have similar meaning."
    "Avoid specifying the names of programming languages, tools, or cloud environments."
    "Try to pick and rephrase each list so that it aligns well with the requirements of the job offer."
    "For each item, explain how it aligns with the job offer."
    "Lets' think step by step."
)

outro_resume_message = (
    "Your task is to improve the candidate's resume."
    "Each job position contains a list of responsibilities and accomplishments that the candidate did."
    "Provide a rephrased version of each position's list."
    "For each position, condense the list to have no more than 10 items each."
    "Do so by rephrasing and merging together items which have similar meaning."
    "Avoid specifying the names of programming languages, tools, or cloud environments."
)


def resume_formatter(resume: Resume, model: str = default_model) -> str:
    """Format a resume."""
    resume_str = str(resume)
    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": f"{intro_resume_message}\n\n```{resume_str}```\n\n{outro_resume_message}",
        },
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
    logging.info(f"Total cost: {calculate_cost(response.usage)}")

    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


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
        # A value around 0.5 or higher can encourage the model to provide more varied rephrasings.
    )
    logging.info(
        f"Tokens usage: "
        f"{response.usage.prompt_tokens} (prompt), "
        f"{response.usage.completion_tokens} (completion), "
        f"{response.usage.total_tokens} (total)"
    )
    logging.info(f"Total cost: {calculate_cost(response.usage)}")

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
    logging.info(f"Total cost: {calculate_cost(response.usage)}")

    response_message = response.choices[0].message
    if response_message.role == "assistant":
        result = response_message.content
    else:
        result = ""
    return result


def resume_formatter_by_chunks(
    resume: Resume, model: str = default_model, offer: Offer = None
) -> str:
    """Format a resume by chunks."""
    resume_copy = copy.deepcopy(resume)

    # Rework the positions one by one
    positions = []
    for position in resume.positions:
        position_formatted = position_formatter(position, model, offer)
        positions.append(position_formatted)
    resume_copy.positions = positions

    # Rework the skills
    skills = []
    skills.extend([skill for position in resume.positions for skill in position.skills])
    skills.extend(resume.skills)
    resume_copy.skills = list(
        map(str.strip, skills_formatter(", ".join(skills)).split(","))
    )
    return str(resume_copy)
