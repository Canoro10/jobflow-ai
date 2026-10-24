from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    company: str = Field(min_length=2, max_length=100)
    position: str = Field(min_length=2, max_length=150)
    description: str
    remote: bool = False
    salary: float | None = Field(default=None, gt=0)
    
class JobUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=2, max_length=100)
    position: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    remote: bool | None = None
    salary: float | None = Field(default=None, gt=0)

class JobResponse(JobCreate):
    id: int

