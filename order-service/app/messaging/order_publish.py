import json

import aio_pika
from aio_pika.abc import (
    AbstractExchange,
)


async def publish_order_paid(
    exchange: AbstractExchange, routing_key: str, data: dict
) -> None:
    message = aio_pika.Message(json.dumps(data).encode())
    print(f"[RABBITMQ SEND] {routing_key}: {data}")

    await exchange.publish(message, routing_key)
