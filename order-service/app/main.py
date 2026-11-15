from contextlib import asynccontextmanager

from app.api.routers.order import router as order_router
from app.database import engine
from app.models import Base
from app.rabbitmq import connect_rabbitmq, start_payment_consume
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    connection = await connect_rabbitmq()
    await start_payment_consume(connection)
    try:
        yield
    finally:
        await connection.close()


app = FastAPI(lifespan=lifespan)

app.include_router(order_router, tags=["order"])
