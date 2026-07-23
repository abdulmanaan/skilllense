from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Load application settings from the .env file."""

    database_url: str
    adzuna_app_id: str
    adzuna_app_key: str

    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str
    jwt_secret: str

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env")

settings = Settings()
