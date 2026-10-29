from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


def create_job(db: Session, job_data: JobCreate) -> Job:
    job = Job(**job_data.model_dump())

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_jobs(
    db: Session,
    remote: bool | None = None,
    min_salary: float | None = None,
    position: str | None = None,
) -> list[Job]:
    statement = select(Job)

    if remote is not None:
        statement = statement.where(Job.remote == remote)

    if min_salary is not None:
        statement = statement.where(Job.salary >= min_salary)

    if position is not None:
        statement = statement.where(
            Job.position.ilike(f"%{position}%")
        )

    return list(db.scalars(statement).all())


def get_job_by_id(db: Session, job_id: int) -> Job | None:
    return db.get(Job, job_id)


def update_job(
    db: Session,
    job: Job,
    job_data: JobUpdate,
) -> Job:
    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(db: Session, job: Job) -> None:
    db.delete(job)
    db.commit()