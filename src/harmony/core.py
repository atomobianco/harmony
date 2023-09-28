from dataclasses import dataclass
from typing import List
from dataclasses import field
from dacite import from_dict
from harmony.parsers import positions_parser, resume_parser


@dataclass
class Task:
    """A task associated with the job position."""

    description: str  # e.g. "Develop marketing strategies"


@dataclass
class Position:
    """A job position hold somewhere during a period of time."""

    title: str  # e.g. "Software Engineer"
    start: str  # e.g. "2019-01-01"
    end: str  # e.g. "2020-01-01"
    location: str  # e.g. "Paris, France"
    tasks: List[Task]  # responsibilities, achievements, accomplishments

    # def __post_init__(self) -> None:
    #     if self.start > self.end:
    #         raise ValueError(
    #             f"Start date ({self.start}) must be before end date ({self.end})"
    #         )


@dataclass
class Resume:
    """A resume of a person, both in raw and parsed form."""

    raw: str  # raw text of the resume, e.g. "John Doe\nSoftware Engineer\n..."
    summary: str = field(default_factory=str)
    positions: List[Position] = field(default_factory=list)

    def __post_init__(self) -> None:
        resume = resume_parser(self.raw)
        self.summary = resume["summary"]
        # positions_parser(self.raw)
        positions = [
            from_dict(data_class=Position, data=p) for p in resume["positions"]
        ]
        self.positions = positions
