from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.service.payment import PaymentService



def get_payment_service(db:Session = Depends(get_db)):
    """Функция для инъекции зависимости PaymentService"""
    return PaymentService(db)