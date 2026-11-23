from app.api.routers.auth import router as auth_router
from app.api.routers.catalog import router as catalog_router
from app.api.routers.orders import router as order_router
from fastapi import APIRouter

router = APIRouter(prefix="/api")
router.include_router(auth_router, tags=["auth"])
router.include_router(catalog_router, tags=["product"])
router.include_router(order_router, tags=["order"])
