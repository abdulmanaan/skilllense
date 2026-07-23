import secrets
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.core.security import create_access_token
from app.models import User
from app.services.github_oauth import build_authorize_url, exchange_code_for_token, fetch_github_profile

router = APIRouter()
FRONTEND_URL = "http://localhost:5173"

@router.get("/github/login")
async def github_login():
    """Send user to GitHub to authorize our app."""
    state = secrets.token_urlsafe(16)
    url = build_authorize_url(state)
    return RedirectResponse(url)

@router.get("/github/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Sends user back here with a temporary code."""
    access_token = await exchange_code_for_token(code)
    profile = await fetch_github_profile(access_token)

    result = await db.execute(select(User).where(User.github_id == profile["id"]))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            github_id=profile["id"],
            github_username=profile["login"],
            avatar_url=profile.get("avatar_url"),
            access_token=access_token,
        )
        db.add(user)
    else:
        user.access_token = access_token
        user.github_username = profile["login"]
        user.avatar_url = profile.get("avatar_url")

    await db.commit()
    await db.refresh(user)

    jwt_token = create_access_token(user.id)
    return RedirectResponse(f"{FRONTEND_URL}/auth/callback?token={jwt_token}")

