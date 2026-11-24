from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STYLEIQ_", env_file=".env", extra="ignore")

    allowed_origins: str = "http://localhost:3000"
    max_upload_mb: int = 10
    max_image_pixels: int = 25_000_000
    job_ttl_seconds: int = 900
    weights_dir: str = "./weights"
    device: str = "auto"
    require_cuda: bool = False

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
