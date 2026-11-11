from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    app_name: str = "Financia API"
    api_prefix: str = "/api/v1"
    database_url: str = f"sqlite:///{(ROOT_DIR / 'data' / 'financia.db').as_posix()}"


settings = Settings()
