from harmony.core import Position, Resume

position_1 = Position(
    role="Software Engineer",
    company="Google",
    start="2019",
    end="2020",
    location="Paris, France",
    tasks=["Develop code"],
)

position_2 = Position(
    role="Software Manager",
    company="Google",
    start="2020",
    end="2021",
    location="Paris, France",
    tasks=["Develop code", "Manage engineers"],
)


def test_position_str():
    position_str = str(position_1)
    expected = (
        "### Software Engineer, Google\n\n2019 - 2020, Paris, France\n\n- Develop code"
    )
    assert position_str == expected


def test_resume_str():
    resume = Resume(summary="The summary", positions=[position_1, position_2])
    resume_str = str(resume)
    expected = (
        "## Summary\n\nThe summary\n\n"
        "## Experience\n\n"
        "### Software Engineer, Google\n\n2019 - 2020, Paris, France\n\n"
        "- Develop code\n\n"
        "### Software Manager, Google\n\n2020 - 2021, Paris, France\n\n"
        "- Develop code\n"
        "- Manage engineers"
    )
    assert resume_str == expected
