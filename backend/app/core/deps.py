from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from app.core.security import decode_access_token
from app.models import User

bearer_scheme = HTTPBearer(auto_error=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for one request, then close it."""
    async with async_session() as session:
        yield session

async def get_user_by_token(token: str, db: AsyncSession) -> User | None:
    """Search for a user by their access token."""
    user_id = decode_access_token(token)
    if user_id is None:
        return None
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get the currently authenticated user based on the access token."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = await get_user_by_token(credentials.credentials, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user
