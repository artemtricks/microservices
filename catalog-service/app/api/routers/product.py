from fastapi import APIRouter, Depends, status
from app.schemas import ProductCreate as ProductCreateSchema, ProductRead as ProductReadSchema
from app.service.products import ProductsService
from app.api.dependencies import get_product_service

router = APIRouter()



@router.get('/products')
def get_products(product_service: ProductsService = Depends(get_product_service)) -> list[ProductReadSchema]:
     return product_service.list_products()
 


@router.post('/products')
def create_products(payload: ProductCreateSchema, product_service: ProductsService = Depends(get_product_service)) -> ProductReadSchema:
    return product_service.create_product(payload)



@router.get('/products/{product_id}')
def get_product(product_id: str, product_service: ProductsService = Depends(get_product_service)) -> ProductReadSchema:
    return product_service.get_one_product(product_id)


