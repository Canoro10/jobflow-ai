from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories import job_repository
from app.schemas.job import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


SessionDep = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(
    job: JobCreate,
    db: SessionDep,
):
    return job_repository.create_job(db, job)


@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: SessionDep,
    remote: bool | None = None,
    min_salary: Annotated[float | None, Query(gt=0)] = None,
    position: Annotated[str | None, Query(min_length=2)] = None,
):
    return job_repository.get_jobs(
        db=db,
        remote=remote,
        min_salary=min_salary,
        position=position,
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: SessionDep,
):
    job = job_repository.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: SessionDep,
):
    job = job_repository.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job_repository.update_job(
        db,
        job,
        job_update,
    )


@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: int,
    db: SessionDep,
):
    job = job_repository.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    job_repository.delete_job(db, job)

    return Response(status_code=204)