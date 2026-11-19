from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql+asyncpg://orders:orders@order-db:5432/orders"
    catalog_service_url: str = "http://127.0.0.1:8001"
    payment_service_url: str = "http://127.0.0.1:8003"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"
    payment_queue_name: str = "payment.results"
    payment_succeeded_routing_key: str = "payment.succeeded"
    payment_exchange_name: str = "payment.events"
    order_paid_routing_key: str = "order.paid"
    order_exchange_name: str = "order.events"
    order_queue_name: str = "order.results"


settings = Settings()
