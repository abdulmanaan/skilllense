from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.deps import get_db
from app.services.pipeline import run_refresh_pipeline

router = APIRouter()


@router.post("/refresh-jobs")
async def refresh_jobs(
    x_admin_key: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Endpoint to manually trigger the job-refresh pipeline. Requires a valid admin key."""
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    return await run_refresh_pipeline(db)
