import asyncio
from app.core.config import settings
from app.core.database import async_session
from app.services.job_fetcher import fetch_adzuna_jobs, fetch_remotive_jobs, filter_relevant_jobs
from app.services.job_store import store_jobs
from app.services.job_analyzer import analyze_jobs, seed_roles_and_skills

async def main() -> None:
    print("Fetching from Remotive...")
    remotive = await fetch_remotive_jobs()
    print(f"  got {len(remotive)} jobs")

    print("Fetching from Adzuna...")
    adzuna = await fetch_adzuna_jobs(settings.adzuna_app_id, settings.adzuna_app_key)
    print(f"  got {len(adzuna)} jobs")

    all_jobs = remotive + adzuna
    relevant = filter_relevant_jobs(all_jobs)
    print(f"Filtered: {len(relevant)} relevant / {len(all_jobs)} total "
          f"({len(all_jobs) - len(relevant)} discarded as non-tech)")

    async with async_session() as session:
        new_count = await store_jobs(session, remotive + adzuna)
        await seed_roles_and_skills(session)
        analyzed = await analyze_jobs(session)

    print(f"Stored {new_count} new jobs.")
    print(f"Analyzed {analyzed} jobs.")

if __name__ == "__main__":
    asyncio.run(main())
