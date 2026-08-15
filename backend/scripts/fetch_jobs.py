import asyncio
from app.core.database import async_session
from app.services.pipeline import run_refresh_pipeline


async def main() -> None:
    """Run the job-refresh pipeline and print the results."""
    async with async_session() as session:
        result = await run_refresh_pipeline(session)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
