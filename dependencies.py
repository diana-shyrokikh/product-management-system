import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic.v1 import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import SessionLocal

from users import schemas
from users.crud import get_user_by_username
from users.utils import (
    ALGORITHM,
    JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY
)

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def common_object_parameters(
        pk: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    return {"db": db, "object_id": pk}


async def get_current_user(
    token: str = Depends(reusable_oauth),
    token_type: str = "access",
    db: AsyncSession = Depends(get_db)
) -> schemas.User:
    secret_key = (
        JWT_SECRET_KEY if token_type == "access"
        else JWT_REFRESH_SECRET_KEY
    )

    try:
        payload = jwt.decode(
            token, secret_key, algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except(jwt.InvalidSignatureError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_username(
        db,
        payload.get("sub")
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
