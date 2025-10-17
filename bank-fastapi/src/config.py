from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    database_url: str
    environment: str = "production"
    jwt_secret: str = "my-secret"
    jwt_algorithm: str = "HS256"
    cors_origins: str = "*"


settings = Settings()
