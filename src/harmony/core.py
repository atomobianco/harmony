from dataclasses import dataclass
from typing import List
from dataclasses import field
import pickle
from pydantic import BaseModel, Field
from instructor import openai_function


class Diploma(BaseModel):
    """Educational background, including schools attended and degrees earned."""

    title: str = Field(
        description="The title of the diploma obtained (e.g. Ph.D. in Computer Science).",
    )
    school: str = Field(
        description="The name of the school (e.g. MIT).",
    )
    location: str = Field(
        description="The city and country where the school is located (e.g. Cambridge, MA).",
    )
    start_date: str = Field(
        description="Start date for the diploma.",
    )
    end_date: str = Field(
        description="End date for the diploma.",
    )

    def __str__(self) -> str:
        diploma_str = (
            f"### {self.title}\n\n"
            f"{self.start_date} - {self.end_date}, {self.school}, {self.location}"
        )
        return diploma_str


class Position(BaseModel):
    """Previous employment."""

    job_title: str = Field(
        description="The job title held at the company (e.g. Software Engineer).",
    )
    company_name: str = Field(
        description="The name of the company (e.g. Google).",
    )
    company_location: str = Field(
        description="The city and country where the company is located (e.g. Paris, France).",
    )
    start_date: str = Field(
        description="Start date for the position.",
    )
    end_date: str = Field(
        description="End date for the position.",
    )
    tasks: list[str] = Field(
        default_factory=list,
        description="Responsibilities or achievements accomplished in this position.",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Generic skills and competencies utilized or gained during this position, if detailed \
        (e.g. Project management, Team Leadership).",
    )
    tools: List[str] = Field(
        default_factory=list,
        description="Specific tools, software stack, frameworks, programming languages used during the position, \
        if detailed (e.g. AWS, Python).",
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


class Resume(BaseModel):
    """A candidate's resume, containing personal and professional details."""

    summary: str = Field(
        default_factory=str,
        description="Brief summary of the candidate's career and goals.",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of skills the candidate has.",
    )
    certifications: List[str] = Field(
        default_factory=list,
        description="Any relevant certifications or licenses held by the candidate.",
    )
    languages: List[str] = Field(
        default_factory=list,
        description="The language and level the candidate is able to speak.",
    )
    experience: List[Position] = Field(
        ...,
        default_factory=list,
        description="List of previous employments, that is, job positions held by the candidate.",
    )
    education: List[Diploma] = Field(
        default_factory=list,
        description="Educational background, including schools attended and degrees earned.",
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
        if self.experience:
            positions_str = "\n\n".join([f"{position}" for position in self.experience])
            experience_str = f"## Experience\n\n{positions_str}"
            resume_str += f"\n\n{experience_str}"
        if self.education:
            diplomas_str = "\n\n".join([f"{diploma}" for diploma in self.education])
            education_str = f"## Education\n\n{diplomas_str}"
            resume_str += f"\n\n{education_str}"
        if self.certifications:
            certs_str = "\n".join([f"- {cert}" for cert in self.certifications])
            resume_str += f"\n\n## Certifications\n\n{certs_str}"
        if self.languages:
            languages_str = "\n".join([f"- {cert}" for cert in self.languages])
            resume_str += f"\n\n## Languages\n\n{languages_str}"

        return resume_str

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str):
        with open(path, "rb") as f:
            return pickle.load(f)


class ResumeExtractor(BaseModel):
    """Extract the candidate's resume from the text."""

    resume: Resume = Field(..., description="The candidate's resume.")


@openai_function
def parse_resume(resume: Resume = Field(..., description="The candidate's resume.")):
    """Extract the candidate's resume from the text."""


@dataclass
class Offer:
    """An offer for a job position."""

    raw: str = field(default_factory=str)

    def __str__(self) -> str:
        return self.raw
