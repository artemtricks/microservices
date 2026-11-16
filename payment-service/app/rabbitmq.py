import json

import aio_pika
from aio_pika.abc import (
    AbstractExchange,
    AbstractRobustChannel,
    AbstractRobustConnection,
)


async def connect_rabbitmq(url: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url)


async def declare_payment_exchange(
    channel: AbstractRobustChannel, exchange_name: str
) -> AbstractExchange:
    return await channel.declare_exchange(exchange_name)


async def event_publish_json(
    exchange: AbstractExchange, routing_key: str, data: dict
) -> None:
    message = aio_pika.Message(json.dumps(data).encode())
    print(f"[RABBITMQ SEND] {routing_key}: {data}")

    await exchange.publish(message, routing_key)
