from datetime import UTC, datetime, timedelta

import jwt
from app.config import settings
from app.models import User
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password=password)


def veryfy_password(password: str, encoded_password: str):
    return password_hash.verify(password=password, hash=encoded_password)


def create_access_token(user: User):
    now = datetime.now(UTC)
    expires_in = now + timedelta(seconds=3600)
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": "user",
        "exp": expires_in,
    }

    token = jwt.encode(
        payload,
        key=settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )
    return token
