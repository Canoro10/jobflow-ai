from sqlalchemy import Boolean, CheckConstraint, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    __table_args__ = (
        CheckConstraint(
            "salary IS NULL OR salary > 0",
            name="ck_jobs_salary_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    position: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    remote: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    salary: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )