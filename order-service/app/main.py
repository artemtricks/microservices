from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine
from app.models import Base
from app.api.routers.order import router as order_router




@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(order_router, tags=['order'])

