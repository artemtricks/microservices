from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = (
        "postgresql+asyncpg://notification:notification@payment-db:5432/notification"
    )
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"
    order_paid_routing_key: str = "order.paid"
    order_exchange_name: str = "order.events"
    order_queue_name: str = "order.results"


settings = Settings()
