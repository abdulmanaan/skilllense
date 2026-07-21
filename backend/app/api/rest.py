from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.models import Job, Role, Skill, job_skills
from app.schemas.responses import RoleOut, SkillDemand

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic liveness check."""
    return {"status": "ok"}

@router.get("/roles", response_model=list[RoleOut])
async def list_roles(db: AsyncSession = Depends(get_db)):
    """Return all roles, with how many jobs currently fall under each."""
    stmt = (
        select(Role.slug, Role.name, func.count(Job.id).label("job_count"))
        .outerjoin(Job, Job.role_id == Role.id)
        .group_by(Role.id)
        .order_by(func.count(Job.id).desc())
    )
    rows = (await db.execute(stmt)).all()
    return [RoleOut(slug=r.slug, name=r.name, job_count=r.job_count) for r in rows]


@router.get("/skills/demand", response_model=list[SkillDemand])
async def skill_demand(role: str | None = None, db: AsyncSession = Depends(get_db)):
    """Return the in demand skills."""
    stmt = (
        select(Skill.name, Skill.category, func.count(job_skills.c.job_id).label("demand"))
        .join(job_skills, job_skills.c.skill_id == Skill.id)
    )
    if role:
        stmt = stmt.join(Job, Job.id == job_skills.c.job_id).join(Role, Role.id == Job.role_id)
        stmt = stmt.where(Role.slug == role)

    stmt = stmt.group_by(Skill.id).order_by(func.count(job_skills.c.job_id).desc()).limit(20)
    rows = (await db.execute(stmt)).all()
    return [SkillDemand(name=r.name, category=r.category, demand=r.demand) for r in rows]
