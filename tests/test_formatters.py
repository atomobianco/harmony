from harmony.utils import parse_file
import harmony.formatters as formatters


def test_position_formatter():
    position = parse_file("./tests/resources/position.md")
    position_formatted = formatters.position_formatter(position)
    assert position_formatted != ""


def test_position_offer_formatter():
    position = parse_file("./tests/resources/position.md")
    offer = parse_file("./tests/resources/offer.md")
    position_formatted = formatters.position_formatter(position, offer)
    assert position_formatted != ""


def test_skills_formatter():
    skills_raw = "Scala, Python, Java, Javascript"
    skills_formatted_response = formatters.skills_formatter(skills_raw)
    assert "Scala" not in skills_formatted_response
