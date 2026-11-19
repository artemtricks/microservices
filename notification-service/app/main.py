from contextlib import asynccontextmanager

from app.api.routers.notification import router as notification_router
from app.database import engine
from app.models import Base
from app.rabbitmq import (
    connect_rabbitmq,
    start_order_paid_consume,
)
from app.service.notification import NotificationService
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
        app.state.notification_service = NotificationService(
            session_factory=session_factory
        )
        await start_order_paid_consume(connection, app.state.notification_service)
        yield
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(notification_router, tags=["notification"])
