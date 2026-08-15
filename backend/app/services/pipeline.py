from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.services.job_analyzer import analyze_jobs, seed_roles_and_skills
from app.services.job_fetcher import fetch_adzuna_jobs, fetch_remotive_jobs, filter_relevant_jobs
from app.services.job_store import store_jobs


async def run_refresh_pipeline(session: AsyncSession) -> dict:
    """Run the job fetching, filtering, storing, and analyzing pipeline."""
    remotive = await fetch_remotive_jobs()
    adzuna = await fetch_adzuna_jobs(settings.adzuna_app_id, settings.adzuna_app_key)

    all_jobs = remotive + adzuna
    relevant = filter_relevant_jobs(all_jobs)

    new_count = await store_jobs(session, relevant)
    await seed_roles_and_skills(session)
    analyzed = await analyze_jobs(session)

    return {
        "fetched_remotive": len(remotive),
        "fetched_adzuna": len(adzuna),
        "relevant": len(relevant),
        "stored_new": new_count,
        "analyzed": analyzed,
    }
