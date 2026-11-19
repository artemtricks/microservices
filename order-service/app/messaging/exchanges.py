from aio_pika.abc import AbstractExchange, AbstractRobustChannel


async def declare_order_exchange(
    channel: AbstractRobustChannel, exchange_name: str
) -> AbstractExchange:
    return await channel.declare_exchange(exchange_name)
