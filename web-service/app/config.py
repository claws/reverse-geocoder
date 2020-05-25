from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    service_name: str = "Reverse Geocoder Service"
    database_dsn: PostgresDsn = "postgresql://postgres:postgres@localhost:54321/postgres"
    database_test: bool = False
    debug: bool = False
    api_v1_path: str = "/v1/reverse-geocoder"
    open_api_path = f"/openapi.json"
    docs_path = f"/docs"

    class Config:
        env_file = ".env"


settings = Settings()
