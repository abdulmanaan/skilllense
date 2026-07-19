import asyncio
from app.core.config import settings
from app.core.database import async_session
from app.services.job_fetcher import fetch_adzuna_jobs, fetch_remotive_jobs
from app.services.job_store import store_jobs

async def main() -> None:
    print("Fetching from Remotive...")
    remotive = await fetch_remotive_jobs()
    print(f"  got {len(remotive)} jobs")

    print("Fetching from Adzuna...")
    adzuna = await fetch_adzuna_jobs(settings.adzuna_app_id, settings.adzuna_app_key)
    print(f"  got {len(adzuna)} jobs")

    async with async_session() as session:
        new_count = await store_jobs(session, remotive + adzuna)

    print(f"Stored {new_count} new jobs.")

if __name__ == "__main__":
    asyncio.run(main())
