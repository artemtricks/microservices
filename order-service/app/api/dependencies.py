from app.clients import CatalogClient, PaymentClient
from app.database import get_db
from app.service.order import OrderService
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_catalog_client(request: Request) -> CatalogClient:
    return request.app.state.catalog_client


def get_payment_client(request: Request) -> PaymentClient:
    return request.app.state.payment_client


def get_order_service(
    db: AsyncSession = Depends(get_db),
    catalog_client: CatalogClient = Depends(get_catalog_client),
    payment_client: PaymentClient = Depends(get_payment_client),
):
    return OrderService(
        db,
        catalog_client,
        payment_client,
    )
