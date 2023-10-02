from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from products import models, schemas


async def get_all_products(
        db: AsyncSession,
) -> list[models.Product]:
    query = select(models.Product)
    product_list = await db.execute(query)
    return [product[0] for product in product_list.fetchall()]


async def get_product(
        db: AsyncSession,
        product_id: int
) -> [models.Product | None]:
    query = select(models.Product).where(
        models.Product.id == product_id
    )
    product = await db.execute(query)
    product = product.fetchone()

    if product:
        return product[0]

    return None


async def create_product(
        db: AsyncSession,
        product: schemas.CreateProduct
) -> dict:
    query = insert(models.Product).values(
        name=product.name,
        description=product.description,
        price=product.price,
    )

    new_product = await db.execute(query)

    await db.commit()

    new_product = {
        **product.model_dump(),
        "id": new_product.lastrowid
    }

    return new_product


async def update_product(
        db: AsyncSession,
        product_id: int,
        new_data: dict,
) -> [models.Product | None]:
    query = select(models.Product).where(
        models.Product.id == product_id
    )
    updated_product = await db.execute(query)
    updated_product = updated_product.fetchone()

    if updated_product:
        updated_product = updated_product[0]

        for field, value in new_data.items():
            setattr(updated_product, field, value)

        await db.commit()
        await db.refresh(updated_product)

        return updated_product

    return None


async def delete_product(
        db: AsyncSession,
        product_id: int,
) -> [dict | bool]:
    query = select(models.Prouct).where(
        models.Product.id == product_id
    )
    deleted_product = await db.execute(query)
    deleted_product = deleted_product.fetchone()

    if deleted_product:
        await db.delete(deleted_product[0])
        await db.commit()

        return {"message": "Product deleted"}

    return False
