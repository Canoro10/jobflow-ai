from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.schemas.job import JobCreate, JobResponse, JobUpdate


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
async def get_jobs(
    remote: bool | None = None,
    min_salary: Annotated[float | None, Query(gt=0)] = None,
    position: Annotated[str | None, Query(min_length=2)] = None,
):
    filtered_jobs = jobs

    if remote is not None:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.remote == remote
        ]

    if min_salary is not None:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.salary is not None and job.salary >= min_salary
        ]

    if position is not None:
        filtered_jobs = [
            job for job in filtered_jobs
            if position.lower() in job.position.lower()
        ]

    return filtered_jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int):
    for job in jobs:
        if job.id == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail="Job not found",
    )
    
@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(job_id: int, job_update: JobUpdate):
    for index, job in enumerate(jobs):
        if job.id == job_id:
            update_data = job_update.model_dump(exclude_unset=True)

            updated_job = job.model_copy(update=update_data)

            jobs[index] = updated_job

            return updated_job

    raise HTTPException(
        status_code=404,
        detail="Job not found",
    )