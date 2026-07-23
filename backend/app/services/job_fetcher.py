import httpx
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from app.services.analyzer import extract_skills

class FetchedJob(BaseModel):
    """Convert fetched job's format into our specified format."""

    source: str
    external_id: str
    title: str
    company: str | None = None
    location: str | None = None
    description: str | None = None
    url: str | None = None
    posted_at: datetime | None = None

    @field_validator("posted_at")
    @classmethod
    def ensure_utc(cls, value: datetime | None) -> datetime | None:
        """Normalize every datetime to timezone-aware UTC."""
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


async def fetch_remotive_jobs() -> list[FetchedJob]:
    """Fetch jobs from Remotive API."""
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        response = await client.get(
            "https://remotive.com/api/remote-jobs",
            params={"category": "software-dev"},
        )
        response.raise_for_status()
        data = response.json()

    jobs: list[FetchedJob] = []
    for item in data.get("jobs", []):
        jobs.append(
            FetchedJob(
                source="remotive",
                external_id=str(item["id"]),
                title=item["title"],
                company=item.get("company_name"),
                location=item.get("candidate_required_location"),
                description=item.get("description"),
                url=item.get("url"),
                posted_at=item.get("publication_date"),
            )
        )
    return jobs

async def fetch_adzuna_jobs(
        app_id: str, app_key: str, country: str = "gb", pages: int = 2
) -> list[FetchedJob]:
    """Fetch jobs from Adzuna API."""
    jobs = []
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        for page in range(1, pages + 1):
            response = await client.get(
                f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
                params={
                    "app_id": app_id,
                    "app_key": app_key,
                    "results_per_page": 50,
                    "category": "it-jobs",
                },
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("results", []):
                jobs.append(
                    FetchedJob(
                        source="adzuna",
                        external_id=str(item["id"]),
                        title=item["display_name"] if isinstance(item.get("display_name"), str) else item["title"],
                        company=(item.get("location") or {}).get("display_name"),
                        location=(item.get("location") or {}).get("display_name"),
                        description=item.get("description"),
                        url=item.get("redirect_url"),
                        posted_at=item.get("created"),
                    )
                )
    return jobs

def filter_relevant_jobs(jobs: list[FetchedJob]) -> list[FetchedJob]:
    """Keep only jobs where at least one known tech skill cna be detected."""
    relevant = []
    for job in jobs:
        skills = extract_skills(job.title, job.description)
        if skills:
            relevant.append(job)
    return relevant
