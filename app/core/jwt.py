from typing import Any, Union
import jwt
from datetime import datetime, timedelta
from core.config import settings
from fastapi.security import OAuth2PasswordBearer


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow(
        ) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow(
        ) + timedelta(minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


config_set_jwt_token_to_head = OAuth2PasswordBearer(
    tokenUrl="auth/get-jwt-token/",
    scheme_name="JWT"
)
