from harmony.utils import parse_file
import harmony.formatters as formatters


def test_position_formatter():
    position_raw = parse_file("./tests/resources/experience.md")
    position_formatted_response = formatters.position_formatter(position_raw)
    assert position_formatted_response != ""


def test_resume_formatter():
    resume_raw = parse_file("./tests/resources/resume.md")
    resume_formatted_response = formatters.position_formatter(resume_raw)
    assert resume_formatted_response != ""


def test_skills_formatter():
    skills_raw = "Scala, Python, Java, Javascript"
    skills_formatted_response = formatters.skills_formatter(skills_raw)
    assert "Scala" not in skills_formatted_response
