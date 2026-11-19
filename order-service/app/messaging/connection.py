import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
)
from app.config import settings


async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)
