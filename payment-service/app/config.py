from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql+psycopg://postgres:admin@localhost:5432/postgres"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"


settings = Settings()
