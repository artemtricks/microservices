from contextlib import asynccontextmanager

from app.api.routers.order import router as order_router
from app.clients import CatalogClient, PaymentClient
from app.config import settings
from app.database import engine
from app.messaging import (
    connect_rabbitmq,
    declare_order_exchange,
)
from app.messaging.payment_consume import start_payment_consume
from app.models import Base
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        connection = await connect_rabbitmq()
        session_factory = async_sessionmaker(
            engine, expire_on_commit=False, autoflush=False
        )
        catalog_client = CatalogClient(settings.catalog_service_url)
        payment_client = PaymentClient(settings.payment_service_url)
        await payment_client.start()
        await catalog_client.start()

        app.state.session_factory = session_factory
        app.state.payment_client = payment_client
        app.state.catalog_client = catalog_client
        app.state.rabbitmq_connection = connection

        channel = await connection.channel()
        app.state.payment_exchange = await declare_order_exchange(
            channel,
            settings.order_exchange_name,
        )

        await start_payment_consume(connection, app)

        yield
        await payment_client.close()
        await catalog_client.close()
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(order_router, tags=["order"])
