from app.database import get_db
from app.service.payment import PaymentService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_payment_service(db: AsyncSession = Depends(get_db)):
    """Функция для инъекции зависимости PaymentService"""
    return PaymentService(db)
