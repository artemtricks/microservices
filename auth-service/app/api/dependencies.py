from app.database import get_db
from app.service.auth import AuthService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_auth_service(db: Session = Depends(get_db)):
    """Функция для инъекции зависимости ProductService"""
    return AuthService(db)
