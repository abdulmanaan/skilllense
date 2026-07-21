from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Job, Role, Skill
from app.services.analyzer import ROLES, classify_role, extract_skills
from app.services.skills_catalog import SKILLS_CATALOG

async def seed_roles_and_skills(session: AsyncSession) -> None:
    """Make sure all roles and skills from our catalogs exist in the DB."""

    # Get existing roles to avoid inserting duplicates
    existing_roles = {r.slug for r in (await session.execute(select(Role))).scalars()}

    # Add missing roles from the application role catalog
    for slug, (name, _, _) in ROLES.items():
        if slug not in existing_roles:
            session.add(Role(name=name, slug=slug))

    existing_skills = {s.name for s in (await session.execute(select(Skill))).scalars()}

    # Add missing skills from the skills catalog
    for name, (category, _) in SKILLS_CATALOG.items():
        if name not in existing_skills:
            session.add(Skill(name=name, category=category))

    await session.commit()


async def analyze_jobs(session: AsyncSession) -> int:
    """Process all jobs that don't have skills assigned yet. Returns count."""

    # Load roles and skills
    roles = {r.slug: r for r in (await session.execute(select(Role))).scalars()}
    skills = {s.name: s for s in (await session.execute(select(Skill))).scalars()}

    result = await session.execute(
        select(Job)
        .options(selectinload(Job.skills))
        .where(~Job.skills.any())
    )
    jobs = result.scalars().all()

    for job in jobs:
        found = extract_skills(job.title, job.description)
        job.skills = [skills[name] for name in found if name in skills]

        role_slug = classify_role(job.title, found)
        job.role = roles.get(role_slug) if role_slug else None

    await session.commit()
    return len(jobs)
