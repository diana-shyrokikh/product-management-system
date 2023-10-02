from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def common_product_parameters(
        product_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    return {"db": db, "product_id": product_id}
