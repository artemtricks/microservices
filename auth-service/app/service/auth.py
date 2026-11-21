from app.repository.auth import AuthRepository
from app.schemas import TokenResponse, UserLogin, UserRead, UserRegister
from app.security import create_access_token, veryfy_password
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.auth_repository = AuthRepository(db)

    def register(self, payload: UserRegister) -> TokenResponse:
        user_orm = self.auth_repository.register(payload=payload)
        self.db.commit()
        access_token = create_access_token(user_orm)
        return TokenResponse(
            access_token=access_token, user=UserRead.model_validate(user_orm)
        )

    def login(self, payload: UserLogin):
        user_orm = self.auth_repository.login(payload=payload)
        if not user_orm:
            raise HTTPException(404, f"User {payload.email} not found")
        if not veryfy_password(
            password=payload.password, encoded_password=user_orm.password_hash
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        access_token = create_access_token(user_orm)
        return TokenResponse(
            access_token=access_token, user=UserRead.model_validate(user_orm)
        )
