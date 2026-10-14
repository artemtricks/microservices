from contextlib import asynccontextmanager

from app.api.routers.payment import router as payment_router
from app.database import engine
from app.models import Base
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(payment_router, tags=["payment"])
