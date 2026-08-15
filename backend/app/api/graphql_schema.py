import strawberry
from sqlalchemy import func, select
from app.api.graphql_types import JobType, RoleType, SkillType, SkillGapType
from app.core.database import async_session
from app.models import Job, Role, Skill, job_skills
from app.services.github_repos import extract_user_skills

async def _top_skills_for_role(role_id: int | None, limit: int = 10) -> list[SkillType]:
    """Return the top skills of a specified role."""
    async with async_session() as session:
        stmt = select(
            Skill.name, Skill.category, func.count(job_skills.c.job_id).label("demand")
        ).join(job_skills, job_skills.c.skill_id == Skill.id)

        if role_id is not None:
            stmt = stmt.join(Job, Job.id == job_skills.c.job_id).where(Job.role_id == role_id)

        stmt = stmt.group_by(Skill.id).order_by(func.count(job_skills.c.job_id).desc()).limit(limit)
        rows = (await session.execute(stmt)).all()
        return [SkillType(name=r.name, category=r.category, demand=r.demand) for r in rows]

@strawberry.type
class Query:
    @strawberry.field
    async def roles(self) -> list[RoleType]:
        """Return all roles with their job counts and top skills."""
        async with async_session() as session:
            stmt = (
                select(Role.id, Role.slug, Role.name, func.count(Job.id).label("job_count"))
                .outerjoin(Job, Job.role_id == Role.id)
                .group_by(Role.id)
                .order_by(func.count(Job.id).desc())
            )
            rows = (await session.execute(stmt)).all()

        return [
            RoleType(
                slug=r.slug,
                name=r.name,
                job_count=r.job_count,
                top_skills=await _top_skills_for_role(r.id),
            )
            for r in rows
        ]

    @strawberry.field
    async def top_skills(self, role: str | None = None, limit: int = 15) -> list[SkillType]:
        """Return overall top skills, or scoped to one role."""
        role_id = None
        if role:
            async with async_session() as session:
                result = await session.execute(select(Role.id).where(Role.slug == role))
                role_id = result.scalar_one_or_none()
        return await _top_skills_for_role(role_id, limit)

    @strawberry.field
    async def jobs_for_role(self, role: str, limit: int = 20) -> list[JobType]:
        """Return sample of actual job posting for one role."""
        async with async_session() as session:
            stmt = (
                select(Job)
                .join(Role, Role.id == Job.role_id)
                .where(Role.slug == role)
                .order_by(Job.posted_at.desc())
                .limit(limit)
            )
            jobs = (await session.execute(stmt)).scalars().all()

        return [
            JobType(
                id=j.id, title=j.title, company=j.company,
                location=j.location, url=j.url, source=j.source,
            )
            for j in jobs
        ]

    @strawberry.field
    async def skill_gap(self, info: strawberry.Info, role: str) -> SkillGapType:
        """Compares the logged-in user's GitHub skills against market
        demand for one role."""
        user = info.context.get("user")
        if user is None:
            raise Exception("Not authenticated")

        async with async_session() as session:
            result = await session.execute(select(Role.id).where(Role.slug == role))
            role_id = result.scalar_one_or_none()
        if role_id is None:
            raise Exception(f"Unknown role: {role}")

        market = await _top_skills_for_role(role_id, limit=25)
        user_skills = await extract_user_skills(user.access_token)

        have = [s for s in market if s.name in user_skills]
        gap = [s for s in market if s.name not in user_skills]
        extra = sorted(user_skills - {s.name for s in market})

        return SkillGapType(have=have, gap=gap, extra=extra)

schema = strawberry.Schema(query=Query)
