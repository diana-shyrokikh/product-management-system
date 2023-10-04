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


async def common_category_parameters(
        category_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    return {"db": db, "category_id": category_id}
