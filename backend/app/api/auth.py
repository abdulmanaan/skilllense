import secrets
from fastapi import APIRouter, Depends, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, get_current_user
from app.core.security import create_access_token
from app.models import User
from app.services.github_oauth import build_authorize_url, exchange_code_for_token, fetch_github_profile
from app.core.config import settings

router = APIRouter()

STATE_COOKIE_NAME = "oauth_state"

@router.get("/github/login")
async def github_login():
    """Send user to GitHub, remembering our 'state' in a cookie."""
    state = secrets.token_urlsafe(16)
    url = build_authorize_url(state)

    response = RedirectResponse(url)
    response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=state,
        max_age=600,
        httponly=True,
        samesite="lax",
    )
    return response

@router.get("/github/callback")
async def github_callback(
        code: str,
        state: str,
        db: AsyncSession = Depends(get_db),
        oauth_state: str | None = Cookie(default=None),
):
    """Sends user back here, verify state, then log them in."""
    if oauth_state is None or state != oauth_state:
        raise HTTPException(status_code=400, detail="Invalid or missing OAuth state")

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
    response = RedirectResponse(f"{settings.frontend_url}/auth/callback?token={jwt_token}")
    response.delete_cookie(STATE_COOKIE_NAME)
    return response

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    """Returns the currently logged-in user's basic info."""
    return {
        "id": user.id,
        "github_username": user.github_username,
        "avatar_url": user.avatar_url,
    }
