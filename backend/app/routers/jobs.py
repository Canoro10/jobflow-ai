from fastapi import APIRouter, HTTPException

from app.schemas.job import JobCreate, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


jobs: list[JobResponse] = []


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(job: JobCreate):
    new_job = JobResponse(
        id=len(jobs) + 1,
        **job.model_dump(),
    )

    jobs.append(new_job)

    return new_job

@router.get("/", response_model=list[JobResponse])
async def get_jobs():
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int):
    for job in jobs:
        if job.id == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail="Job not found",
    )