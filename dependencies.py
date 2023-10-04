from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def common_object_parameters(
        pk: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    return {"db": db, "object_id": pk}
