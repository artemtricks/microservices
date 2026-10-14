import json

import aio_pika
from aio_pika.abc import AbstractExchange, AbstractRobustConnection
from aiormq.abc import AbstractChannel


async def connect_rabitmq(url: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url)


async def declare_payment_exchange(channel: AbstractChannel, exchange_name: str):
    return await channel.exchange_declare(exchange_name)


async def event_publish_json(exchange: AbstractExchange, routing_key: str, data: dict):
    message = aio_pika.Message(json.dumps(data).encode())
    await exchange.publish(message, routing_key)
