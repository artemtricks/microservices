from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.service.order import OrderService



def get_order_service(db:Session = Depends(get_db)):
    """Функция для инъекции зависимости OrderService"""
    return OrderService(db)