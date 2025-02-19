from harmony.core import Position, Resume

position_1 = Position(
    job_title="Software Engineer",
    company_name="Google",
    start_date="2019",
    end_date="2020",
    company_location="Paris, France",
    tasks=["Develop code"],
)

position_2 = Position(
    job_title="Software Manager",
    company_name="Google",
    start_date="2020",
    end_date="2021",
    company_location="Paris, France",
    tasks=["Develop code", "Manage engineers"],
)

certifications = ["Scrum master academy", "Software engineering academy"]

resume = Resume(
    summary="The summary",
    experience=[position_1, position_2],
    certifications=certifications,
)


def test_position_str():
    position_str = str(position_1)
    expected = (
        "### Software Engineer, Google\n\n2019 - 2020, Paris, France\n\n- Develop code"
    )
    assert position_str == expected


def test_resume_str():
    resume_str = str(resume)
    expected = (
        "## Summary\n\nThe summary\n\n"
        "## Experience\n\n"
        "### Software Engineer, Google\n\n2019 - 2020, Paris, France\n\n"
        "- Develop code\n\n"
        "### Software Manager, Google\n\n2020 - 2021, Paris, France\n\n"
        "- Develop code\n"
        "- Manage engineers\n\n"
        "## Certifications\n\n"
        "- Scrum master academy\n"
        "- Software engineering academy"
    )
    assert resume_str == expected
