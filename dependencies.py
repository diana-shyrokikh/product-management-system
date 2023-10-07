from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import SessionLocal

from users import schemas
from users.crud import get_user_by_username
from users.utils import verify_token

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def common_object_parameters(
        object_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    return {"db": db, "object_id": object_id}


async def get_current_user(
    token: str = Depends(reusable_oauth),
    db: AsyncSession = Depends(get_db)
) -> schemas.User:
    payload = verify_token(
        token=token,
        token_type="access",
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


def is_admin(
    user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
        )

    return user
