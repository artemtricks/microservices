from app.clients.catalog_client import CatalogClient
from app.database import get_db
from app.service.order import OrderService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_order_service(db: Session = Depends(get_db)):
    """Функция для инъекции зависимости OrderService"""
    catalog_client = CatalogClient(base_url="products")
    return OrderService(db, catalog_client)
