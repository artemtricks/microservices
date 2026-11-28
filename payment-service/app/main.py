from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from app.api.routers.payment import router as payment_router
from app.config import settings
from app.database import engine
from app.kafka import create_kafka_producer
from app.models import Base
from app.rabbitmq import connect_rabbitmq, declare_payment_exchange
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as database_connection:
        await database_connection.run_sync(Base.metadata.create_all)
        rabbitmq_connection = await connect_rabbitmq(url=settings.rabbitmq_url)
        channel = await rabbitmq_connection.channel()
        kafka_producer: AIOKafkaProducer = create_kafka_producer()
        await kafka_producer.start()
        app.state.payment_exchange = await declare_payment_exchange(
            channel, settings.payment_exchange_name
        )
        app.state.kafka_producer = kafka_producer
    try:
        yield
    finally:
        await kafka_producer.stop()
        await rabbitmq_connection.close()


app = FastAPI(lifespan=lifespan)

app.include_router(payment_router, tags=["payment"])
