from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Job
from app.services.job_fetcher import FetchedJob

async def store_jobs(session: AsyncSession, jobs: list[FetchedJob]) -> int:
    """Inserts jobs into database and returns count of new rows."""
    if not jobs:
        return 0

    stmt = (
        insert(Job)
        .values([job.model_dump() for job in jobs])
        .on_conflict_do_nothing(constraint="uq_job_source_external_id")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount
