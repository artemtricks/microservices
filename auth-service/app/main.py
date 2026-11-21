from contextlib import asynccontextmanager

from app.api.routers.auth import router as auth_router
from app.database import engine
from app.models import Base
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=["auth"])
