from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Table, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

# Association table
job_skills = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)          # "Backend Developer"
    slug: Mapped[str] = mapped_column(unique=True)          # "backend-developer"

    jobs: Mapped[list["Job"]] = relationship(back_populates="role")


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)          # "Python"
    category: Mapped[str | None]                            # "language", "framework", ...

    jobs: Mapped[list["Job"]] = relationship(
        secondary=job_skills, back_populates="skills"
    )


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (
        # Store the same job only once
        UniqueConstraint("source", "external_id", name="uq_job_source_external_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str]                                     # Source of API
    external_id: Mapped[str]                                # the job's id in that API
    title: Mapped[str]
    company: Mapped[str | None]
    location: Mapped[str | None]
    description: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str | None]
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Role | None] = relationship(back_populates="jobs")

    skills: Mapped[list[Skill]] = relationship(
        secondary=job_skills, back_populates="jobs"
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    github_id: Mapped[int] = mapped_column(unique=True, index=True)
    github_username: Mapped[str]
    avatar_url: Mapped[str | None]
    access_token: Mapped[str]
    createt_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
