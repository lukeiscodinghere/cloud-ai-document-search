from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    environment: str = "local"   # local | production
    log_level: str = "INFO"

settings = Settings()
