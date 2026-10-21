from fastapi import APIRouter

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

