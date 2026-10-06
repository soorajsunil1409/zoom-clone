from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./zoom.db"
    frontend_url: str = "http://localhost:3000"

    max_participants: int = 6

    cloudflare_turn_key_id: str = ""
    cloudflare_turn_api_token: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()