import os
from datetime import datetime, timedelta
from typing import Union, Any

from dotenv import load_dotenv
import jwt
from passlib.context import CryptContext

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(
        password: str, hashed_pass: str
) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(
        subject: Union[str, Any],
        token_type: str,
        expires_delta: int = None
) -> str:
    if expires_delta:
        expires_delta = datetime.now() + timedelta(
            minutes=expires_delta
        )
    else:
        token_expire_minutes = (
            ACCESS_TOKEN_EXPIRE_MINUTES
            if token_type == "access"
            else REFRESH_TOKEN_EXPIRE_MINUTES
        )
        expires_delta = datetime.now() + timedelta(
            minutes=token_expire_minutes
        )

    to_encode = {
        "exp": expires_delta.timestamp(),
        "sub": str(subject)
    }
    secret_key = (
        JWT_SECRET_KEY if token_type == "access"
        else JWT_REFRESH_SECRET_KEY
    )
    encoded_jwt = jwt.encode(
        to_encode, secret_key, ALGORITHM
    )

    return encoded_jwt
