import httpx
from app.core.config import settings

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"

def build_authorize_url(state: str) -> str:
    """The URL we redirect the user to, to start GitHub login."""
    params = {
        "client_id": settings.github_client_id,
        "redirect_url": settings.github_redirect_uri,
        "scope": "read:user repo",
        "state": state,
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{GITHUB_AUTHORIZE_URL}?{query}"

async def exchange_code_for_token(code: str) -> str:
    """Trade the temporary 'code' GitHub gave us for a real access token."""
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_url": settings.github_redirect_uri,
            },
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        data = response.json()

    if "access_token" not in data:
        raise ValueError(f"GitHub did not return a token: {data}")
    return data["access_token"]

async def fetch_github_profile(access_token: str) -> dict:
    """Get the logged-in user's basic profile."""
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )
        response.raise_for_status()
        return response.json()
