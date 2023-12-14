from harmony.utils import parse_file
import harmony.parsers as parsers
import pytest


@pytest.fixture()
def resume_raw():
    return parse_file("./tests/resources/resume.md")


@pytest.fixture()
def resume_parsed(resume_raw):
    return parsers.resume_parser(resume_raw)


def test_resume_parser(resume_parsed):
    assert len(resume_parsed.experience) == 2
    assert len(resume_parsed.skills) in [12, 13]
    assert len(resume_parsed.education) == 1


def test_resume_parser_experience(resume_parsed):
    experience = sorted(
        resume_parsed.experience, key=lambda x: x.start_date, reverse=True
    )
    assert len(experience) == 2

    experience_one = experience[0]
    assert experience_one.job_title == "Senior Software Engineer"
    assert experience_one.company_name == "XYZ Tech"
    assert experience_one.start_date == "2019"
    assert len(experience_one.tasks) == 3
    assert experience_one.skills == []
    assert experience_one.tools == []

    experience_two = experience[1]
    assert experience_two.job_title == "Software Engineer"
    assert experience_two.company_name == "ABC Solutions"
    assert experience_two.start_date == "2016"
    assert len(experience_two.tasks) == 3
    assert experience_two.skills == []
    assert experience_two.tools == ["AngularJS"]
