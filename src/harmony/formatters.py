system_message = (
    "Ignore all previous instructions. "
    "From this point forward, you are a professional recruiter with years of experience analysing and improving "
    "Curriculum Vitae (CV) and resumes."
)

intro_tasks_message = (
    "Here follows, surrounded by triple back ticks, a list of tasks that a candidate was responsible and accomplished "
    "during his job."
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
