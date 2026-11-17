import json
from functools import partial

import aio_pika
from aio_pika.abc import (
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractRobustConnection,
)
from app.config import settings
from app.schemas import NotificationCreateSchema
from app.service.notification import NotificationService


async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)


async def handle_notification_events(
    message: AbstractIncomingMessage, notification_service: NotificationService
):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))
        if event is not None:
            payload = NotificationCreateSchema(
                order_id=event["order_id"],
                user_id=event["user_id"],
                message=f"Заказа {event['order_id']} успешно оплачен",
            )
        await notification_service.create(payload=payload)


async def start_order_paid_consume(
    connection: AbstractConnection, notification_service: NotificationService
):
    channel = await connection.channel()
    order_exchange = await channel.declare_exchange(settings.order_exchange_name)
    order_queue = await channel.declare_queue(settings.order_queue_name)
    await order_queue.bind(order_exchange, routing_key=settings.order_paid_routing_key)
    await order_queue.consume(
        partial(handle_notification_events, notification_service=notification_service)
    )
