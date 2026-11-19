import json
from functools import partial

from aio_pika.abc import (
    AbstractConnection,
    AbstractExchange,
    AbstractIncomingMessage,
)
from app.config import settings
from app.messaging import publish_order_paid
from app.service.order import OrderService
from fastapi import FastAPI


async def handle_payment_events(
    message: AbstractIncomingMessage,
    app: FastAPI,
    order_exchange: AbstractExchange,
):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))
        async with app.state.session_factory() as db:
            service = OrderService(
                db=db,
                catalog_client=app.state.catalog_client,
                payment_client=app.state.payment_client,
            )
            order_paid_event = await service.handle_payment_succeeded(event=event)
            if order_paid_event is not None:
                await publish_order_paid(
                    exchange=order_exchange,
                    routing_key=settings.order_paid_routing_key,
                    data=order_paid_event,
                )


async def start_payment_consume(
    connection: AbstractConnection,
    app: FastAPI,
):
    channel = await connection.channel()
    payment_exchange = await channel.declare_exchange(settings.payment_exchange_name)
    payment_queue = await channel.declare_queue(settings.payment_queue_name)
    order_exchange = await channel.declare_exchange(
        settings.order_exchange_name,
        durable=False,
    )
    await payment_queue.bind(
        payment_exchange, routing_key=settings.payment_succeeded_routing_key
    )
    await payment_queue.consume(
        partial(
            handle_payment_events,
            app=app,
            order_exchange=order_exchange,
        )
    )
