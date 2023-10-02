from dataclasses import dataclass
from typing import List
from dataclasses import field


@dataclass
class Position:
    """A job position hold somewhere during a period of time."""

    role: str  # e.g. "Software Engineer"
    company: str  # e.g. "Google"
    start: str  # e.g. "2019-01-01"
    end: str  # e.g. "2020"
    location: str  # e.g. "Paris, France"
    tasks: List[str]  # responsibilities, achievements, accomplishments

    def __str__(self) -> str:
        tasks_str = "\n".join([f"- {task}" for task in self.tasks])
        return f"### {self.role}, {self.company}\n\n{self.start} - {self.end}, {self.location}\n\n{tasks_str}"


@dataclass
class Resume:
    """A resume of a person, both in raw and parsed form."""

    raw: str = field(default_factory=str)
    summary: str = field(default_factory=str)
    positions: List[Position] = field(default_factory=list)

    def __str__(self) -> str:
        summary_str = f"## Summary\n\n{self.summary}"
        positions_str = "\n\n".join([f"{position}" for position in self.positions])
        experience_str = f"## Experience\n\n{positions_str}"
        return f"{summary_str}\n\n{experience_str}"


@dataclass
class Offer:
    """An offer of a job position."""

    raw: str  # raw text of the offer, e.g. "DevOps Engineer\nAs a DevOps Engineer, you will:\n..."
