from dataclasses import dataclass
from typing import List
from dataclasses import field


@dataclass
class Task:
    """A task associated with the job position."""

    description: str  # e.g. "Develop marketing strategies"


@dataclass
class Result:
    """A result expected or accomplished during a job position."""

    description: str  # e.g. "Improved brand visibility"

    def __repr__(self) -> str:
        return f"Result(description={self.description})"


@dataclass
class Position:
    """A job position hold somewhere during a period of time."""

    title: str  # e.g. "Software Engineer"
    start: str  # e.g. "2019-01-01"
    end: str  # e.g. "2020-01-01"
    location: str  # e.g. "Paris, France"
    results: List[Result]
    tasks: List[Task]

    def __str__(self) -> str:
        return f"{self.title} ({self.start} - {self.end})"

    def __repr__(self) -> str:
        return f"Position(title={self.title}, start={self.start}, end={self.end}, location={self.location}, results=[{len(self.results)}], tasks=[{len(self.tasks)}])"

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(
                f"Start date ({self.start}) must be before end date ({self.end})"
            )


@dataclass
class Resume:
    """A resume of a person, both in raw and parsed form."""

    raw: str  # e.g. "John Doe\nSoftware Engineer\n..."
    positions: List[Position] = field(default_factory=list)
