from harmony.core import Resume
import openai
from dotenv import load_dotenv
import os
import logging
from harmony.utils import num_tokens_from_messages, calculate_cost

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

model_name = "gpt-3.5-turbo-16k"

system_message = (
    "Ignore all previous instructions. "
    "From this point forward, you are a professional recruiter with years of experience analysing and improving "
    "Curriculum Vitae (CV) and resumes."
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


def resume_formatter(resume: Resume) -> str:
    """Parse a resume and return a list of positions."""
    resume_str = str(resume)
    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": f"{intro_resume_message}\n\n```{resume_str}```\n\n{outro_resume_message}",
        },
    ]
    logging.info(f"Tokens messages: {num_tokens_from_messages(messages, model_name)}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
    )
    logging.info(
        f"Tokens usage: "
        f"{response.usage.prompt_tokens} (prompt), "
        f"{response.usage.completion_tokens} (completion), "
        f"{response.usage.total_tokens} (total)"
    )
    logging.info(f"Total cost: {calculate_cost(response.usage)}")

    response_message = response["choices"][0]["message"]
    return response_message
