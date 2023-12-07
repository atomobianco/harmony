from dataclasses import dataclass
from typing import List
from dataclasses import field
from pydantic import BaseModel, Field
from instructor import openai_function


class Position(BaseModel):
    """A candidate job position"""

    job_title: str = Field(
        description="The job title held at the company.",
        examples=["Software Engineer"],
    )
    company_name: str = Field(
        description="The name of the company.",
        examples=["Google"],
    )
    company_location: str = Field(
        description="The city and country where the company is located.",
        examples=["Paris, France"],
    )
    start_date: str = Field(
        description="Start date for the position.",
        examples=["2019"],
    )
    end_date: str = Field(
        description="End date for the position.",
        examples=["2019"],
    )
    tasks: list[str] = Field(
        description="Responsibilities or achievements accomplished in this position.",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Skills utilized or gained during this position.",
        examples=["Project management", "Career development"],
    )
    tools: List[str] = Field(
        default_factory=list,
        description="Tools, software stack, or programming languages used during the position.",
        examples=["AWS", "Python"],
    )

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


class PositionsExtractor(BaseModel):
    """Extract the candidate's job positions from the text."""

    positions: List[Position] = Field(..., description="The extracted positions.")


@openai_function
def parse_positions(
    positions: List[Position],
):
    """Extract the candidate's job positions from the text."""


class Resume(BaseModel):
    """A candidate's resume"""

    summary: str = Field(
        default_factory=str, description="The summary of the candidate."
    )
    skills: List[str] = Field(
        default_factory=list, description="The skills of the candidate."
    )
    positions: List[Position] = Field(
        ..., default_factory=list, description="The positions of the candidate."
    )

    def __str__(self) -> str:
        resume_str = ""
        if self.summary:
            resume_str += f"## Summary\n\n{self.summary}"
        if self.skills:
            skills_str = (
                ", ".join(self.skills) if type(self.skills) is list else self.skills
            )
            resume_str += f"\n\n## Skills\n\n{skills_str}"
        if self.positions:
            positions_str = "\n\n".join([f"{position}" for position in self.positions])
            experience_str = f"## Experience\n\n{positions_str}"
            resume_str += f"\n\n{experience_str}"
        return resume_str


class ResumeExtractor(BaseModel):
    """Extract the candidate's resume from the text."""

    resume: Resume = Field(..., description="The extracted resume.")


@dataclass
class Offer:
    """An offer of a job position."""

    raw: str = field(default_factory=str)

    def __str__(self) -> str:
        return self.raw
