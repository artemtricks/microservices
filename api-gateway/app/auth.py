import jwt
from app.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, ValidationError


class CurrentUser(BaseModel):
    id: str
    email: EmailStr


def decode_access_token(token: str) -> CurrentUser:
    print("[TOKEN]:", token)
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
        print("[PAYLOAD_DECODE]:", payload)
        return CurrentUser(id=payload["user_id"], email=payload["email"])
    except (jwt.PyJWTError, ValidationError) as exc:
        print("[JWT ERROR]:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
) -> CurrentUser:
    print("[CREDATIONALS]:", credentials)
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return decode_access_token(token=credentials.credentials)
