from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    """A task associated with the job position."""
    description: str  # e.g. "Develop marketing strategies"


@dataclass
class Result:
    """A result expected or accomplished during a job position."""
    description: str  # e.g. "Improved brand visibility"


@dataclass
class Position:
    """A job position hold somewhere during a period of time."""
    title: str  # e.g. "Software Engineer"
    start: str  # e.g. "2019-01-01"
    end: str  # e.g. "2020-01-01"
    location: str  # e.g. "Paris, France"
    results: List[Result]
    tasks: List[Task]

    def __str__(self):
        return f"{self.title} ({self.start} - {self.end})"

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"Start date ({self.start}) must be before end date ({self.end})")

