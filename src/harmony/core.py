from dataclasses import dataclass
from typing import List
from dataclasses import field


@dataclass
class Position:
    """A job position hold somewhere during a period of time."""

    job_title: str  # The official title held at the company, e.g. Software Engineer
    company_name: str  # The name of the company or organization where one worked, e.g. Google
    company_location: str  # The city and country where the company is located, e.g. Paris, France
    start_date: str  # Start date for the position, e.g. 2019
    end_date: str  # End date for the position, e.g. 2019
    tasks: List[str]  # Responsibilities and achievements accomplished in this position
    skills: List[str] = field(
        default_factory=list
    )  # Skills utilized or gained during this job
    tools: List[str] = field(
        default_factory=list
    )  # Tools, software, or programming languages used in this role

    def __str__(self) -> str:
        tasks_str = "\n".join([f"- {task}" for task in self.tasks])
        skills_str = ", ".join([f"{skill}" for skill in self.skills])
        tools_str = ", ".join([f"{tool}" for tool in self.tools])
        position_str = (
            f"### {self.job_title}, {self.company_name}\n\n"
            f"{self.start_date} - {self.end_date}, {self.company_location}\n\n"
            f"{tasks_str}"
        )
        if skills_str:
            position_str += f"\n\nSkills: {skills_str}"
        if tools_str:
            position_str += f"\n\nTools: {tools_str}"
        return position_str


@dataclass
class Resume:
    """A resume of a person, both in raw and parsed form."""

    raw: str = field(default_factory=str)
    summary: str = field(default_factory=str)
    skills: List[str] = field(default_factory=list)
    positions: List[Position] = field(default_factory=list)

    def __str__(self) -> str:
        resume_str = ""
        if self.summary:
            resume_str += f"## Summary\n\n{self.summary}"
        if self.skills:
            resume_str += f"\n\n## Skills\n\n{self.skills}"
        if self.positions:
            positions_str = "\n\n".join([f"{position}" for position in self.positions])
            experience_str = f"## Experience\n\n{positions_str}"
            resume_str += f"\n\n{experience_str}"
        return resume_str


@dataclass
class Offer:
    """An offer of a job position."""

    raw: str = field(default_factory=str)

    def __str__(self) -> str:
        return self.raw
