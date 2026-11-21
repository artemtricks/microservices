from app.api.dependencies import get_auth_service
from app.schemas import TokenResponse, UserLogin, UserRegister
from app.service.auth import AuthService
from fastapi import APIRouter, Depends, status

router = APIRouter()


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
def register(
    payload: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return auth_service.register(payload=payload)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return auth_service.login(payload=payload)
