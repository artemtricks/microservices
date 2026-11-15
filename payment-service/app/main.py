from contextlib import asynccontextmanager

from app.api.routers.payment import router as payment_router
from app.config import settings
from app.database import engine
from app.models import Base
from app.rabbitmq import connect_rabbitmq, declare_payment_exchange
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        connection = await connect_rabbitmq(url=settings.rabbitmq_url)
        channel = await connection.channel()
        app.state.payment_exchange = await declare_payment_exchange(
            channel, settings.payment_exchange_name
        )
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(payment_router, tags=["payment"])
