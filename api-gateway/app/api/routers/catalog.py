from app.api_clients import request_service
from app.config import settings
from app.schemas import ProductRead as ProductReadSchema
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["product"])


@router.get("/")
async def get_products() -> list[ProductReadSchema]:
    return await request_service(
        method="GET", url=f"{settings.CATALOG_SERVICE_URL}/products"
    )


@router.get("/{product_id}")
async def get_product(product_id: str) -> ProductReadSchema:
    return await request_service(
        method="GET",
        url=f"{settings.CATALOG_SERVICE_URL}/products/{product_id}",
    )
