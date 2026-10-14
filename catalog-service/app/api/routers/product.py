from app.api.dependencies import get_product_service
from app.schemas import ProductCreate as ProductCreateSchema
from app.schemas import ProductRead as ProductReadSchema
from app.service.products import ProductsService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/products")
def get_products(
    product_service: ProductsService = Depends(get_product_service),
) -> list[ProductReadSchema]:
    return product_service.list_products()


@router.post("/products")
def create_products(
    payload: ProductCreateSchema,
    product_service: ProductsService = Depends(get_product_service),
) -> ProductReadSchema:
    return product_service.create_product(payload)


@router.get("/products/{product_id}")
def get_product(
    product_id: str, product_service: ProductsService = Depends(get_product_service)
) -> ProductReadSchema:
    return product_service.get_one_product(product_id)
