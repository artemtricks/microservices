from app.models import User
from app.schemas import UserLogin, UserRegister
from app.security import hash_password
from sqlalchemy import select
from sqlalchemy.orm import Session


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def register(self, payload: UserRegister) -> User:
        user = User(email=payload.email, password_hash=hash_password(payload.password))
        self.db.add(user)
        return user

    def login(self, payload: UserLogin) -> User | None:
        user = self.db.scalar(select(User).where(User.email == str(payload.email)))
        return user
