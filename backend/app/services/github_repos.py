import httpx
from app.services.analyzer import extract_skills

GITHUB_REPOS_URL = "https://api.github.com/user/repos"


async def fetch_user_repos(access_token: str, limit: int = 100) -> list[dict]:
    """Fetch the user's GitHub repos."""
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            GITHUB_REPOS_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
            params={"per_page": limit, "sort": "pushed", "affiliation": "owner"},
        )
        response.raise_for_status()
        return response.json()


async def extract_user_skills(access_token: str) -> set[str]:
    """Extract skills from a user's GitHub repos."""
    repos = await fetch_user_repos(access_token)

    skills: set[str] = set()
    for repo in repos:
        # Skip forked repos
        if repo.get("fork"):
            continue

        language = repo.get("language")
        if language:
            skills |= extract_skills(language, None)

        text = f"{repo.get('name', '')} {repo.get('description', '') or ''}"
        skills |= extract_skills(text, None)

    return skills
