from harmony.utils import parse_file
import harmony.parsers as parsers


def test_positions_parser_from_position():
    position_raw = parse_file("./tests/resources/position.md")
    positions_parsed = parsers.positions_parser(position_raw)
    assert len(positions_parsed) == 1
    assert len(positions_parsed[0].tasks) == 3
    assert positions_parsed[0].start_date == "2016"
    assert positions_parsed[0].end_date == "2019"


def test_positions_parser_from_resume():
    resume_raw = parse_file("./tests/resources/resume.md")
    positions_parsed = parsers.positions_parser(resume_raw)
    assert len(positions_parsed) == 2


def test_resume_parser():
    resume_raw = parse_file("./tests/resources/resume.md")
    resume_parsed = parsers.resume_parser(resume_raw)
    assert resume_parsed
    assert len(resume_parsed.positions) == 2
    assert len(resume_parsed.skills) == 13


def test_resume_vs_positions_parser():
    resume_raw = parse_file("./tests/resources/resume.md")
    resume_parsed = parsers.resume_parser(resume_raw)
    positions_parsed = parsers.positions_parser(resume_raw)
    assert len(resume_parsed.positions) == len(positions_parsed)
    for pos in resume_parsed.positions:
        assert pos in positions_parsed
