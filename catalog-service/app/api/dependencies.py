from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.service.products import ProductsService



def get_product_service(db:Session = Depends(get_db)):
    """Функция для инъекции зависимости ProductService"""
    return ProductsService(db)

