from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(
    job: JobCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_job = Job(**job.model_dump())

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


@router.get("/", response_model=list[JobResponse])
async def get_jobs(
    db: Annotated[Session, Depends(get_db)],
    remote: bool | None = None,
    min_salary: Annotated[float | None, Query(gt=0)] = None,
    position: Annotated[str | None, Query(min_length=2)] = None,
):
    statement = select(Job)

    if remote is not None:
        statement = statement.where(Job.remote == remote)

    if min_salary is not None:
        statement = statement.where(Job.salary >= min_salary)

    if position is not None:
        statement = statement.where(
            Job.position.ilike(f"%{position}%")
        )

    jobs = db.scalars(statement).all()

    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    update_data = job_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    db.delete(job)
    db.commit()

    return Response(status_code=204)