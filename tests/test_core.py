from harmony.core import *


def test_position():
    position = Position(
        title="Software Engineer",
        start="2019-01-01",
        end="2020-01-01",
        location="Paris, France",
        results=[Result(description="Improved brand visibility")],
        tasks=[Task(description="Develop marketing strategies")],
    )
    assert position.title == "Software Engineer"
    assert position.start == "2019-01-01"
    assert position.end == "2020-01-01"
    assert position.location == "Paris, France"
    assert len(position.results) == 1
    assert len(position.tasks) == 1


def test_position_str():
    position = Position(
        title="Software Engineer",
        start="2019-01-01",
        end="2020-01-01",
        location="Paris, France",
        results=[Result(description="Improved brand visibility")],
        tasks=[Task(description="Develop marketing strategies")],
    )
    assert str(position) == "Software Engineer (2019-01-01 - 2020-01-01)"


def test_position_repr():
    position = Position(
        title="Software Engineer",
        start="2019-01-01",
        end="2020-01-01",
        location="Paris, France",
        results=[Result(description="Improved brand visibility")],
        tasks=[Task(description="Develop marketing strategies")],
    )
    assert (
        repr(position)
        == "Position(title=Software Engineer, start=2019-01-01, end=2020-01-01, location=Paris, France, results=[1], tasks=[1])"
    )
