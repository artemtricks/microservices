from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine
from app.models import Base
from app.api.routers.payment import router as payment_router




@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(payment_router, tags=['payment'])

