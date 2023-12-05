from harmony.utils import parse_file
import harmony.parsers as parsers


def test_positions_parser():
    resume_raw = parse_file("./tests/resources/resume.md")
    positions_parsed = parsers.positions_parser(resume_raw)
    assert len(positions_parsed) == 2


def test_positions_parser_2():
    position_raw = parse_file("./tests/resources/position.md")
    positions_parsed = parsers.positions_parser(position_raw)
    assert len(positions_parsed) == 1


def test_resume_parser():
    resume_raw = parse_file("./tests/resources/resume.md")
    resume_parsed = parsers.resume_parser(resume_raw)
    assert resume_parsed
