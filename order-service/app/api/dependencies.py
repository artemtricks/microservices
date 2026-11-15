from app.clients import CatalogClient, PaymentClient
from app.config import settings
from app.database import get_db
from app.service.order import OrderService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_catalog_client() -> CatalogClient:
    return CatalogClient(settings.catalog_service_url)


def get_paymnt_client() -> PaymentClient:
    return PaymentClient(settings.payment_service_url)


def get_order_service(db: Session = Depends(get_db)):
    """Функция для инъекции зависимости OrderService"""
    catalog_client: CatalogClient = Depends(get_catalog_client)
    payment_client: PaymentClient = Depends(get_paymnt_client)
    return OrderService(db, catalog_client, payment_client)
