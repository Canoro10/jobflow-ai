from typing import Literal

from pydantic import BaseModel, Field


class JobAnalysisRequest(BaseModel):
    description: str = Field(min_length=30)


class JobAnalysisResponse(BaseModel):
    position: str | None = None

    seniority: Literal[
        "Intern",
        "Junior",
        "Mid",
        "Senior",
        "Lead",
        "Unknown",
    ]

    skills: list[str]

    remote: bool | None = None
    location: str | None = None
    experience_required: str | None = None