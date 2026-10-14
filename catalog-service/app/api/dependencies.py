from app.database import get_db
from app.service.products import ProductsService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_product_service(db: Session = Depends(get_db)):
    """Функция для инъекции зависимости ProductService"""
    return ProductsService(db)
