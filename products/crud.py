import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from products import models, schemas


async def get_all_products(
        db: AsyncSession,
) -> list[models.Product]:
    query = select(models.Product)
    product_list = await db.execute(query)
    return [
        product[0]
        for product
        in product_list.fetchall()
    ]


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


async def get_product_by_name(
        db: AsyncSession,
        product_name: str
) -> [models.Product | None]:
    query = select(models.Product).where(
        models.Product.name == product_name
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
    product.name = product.name.strip().capitalize()
    product.description = product.description.strip()

    query = insert(models.Product).values(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )

    new_product = await db.execute(query)

    await db.commit()

    new_product = {
        **product.model_dump(),
        "id": new_product.lastrowid,
        "created_at": datetime.datetime.now()
    }

    return new_product


async def update_product(
        db: AsyncSession,
        product_id: int,
        new_data: schemas.UpdateProduct,
) -> [models.Product | None]:
    query = select(models.Product).where(
        models.Product.id == product_id
    )
    updated_product = await db.execute(query)
    updated_product = updated_product.fetchone()

    if updated_product:
        updated_product = updated_product[0]

        if new_data.name:
            updated_product.name = new_data.name.strip().capitalize()
        if new_data.description:
            updated_product.description = new_data.description.strip()
        if new_data.price:
            updated_product.price = new_data.price
        if new_data.category_id:
            updated_product.category_id = new_data.category_id

        await db.commit()
        await db.refresh(updated_product)

        return updated_product

    return None


async def delete_product(
        db: AsyncSession,
        product_id: int,
) -> [dict | bool]:
    query = select(models.Product).where(
        models.Product.id == product_id
    )
    deleted_product = await db.execute(query)
    deleted_product = deleted_product.fetchone()

    if deleted_product:
        await db.delete(deleted_product[0])
        await db.commit()

        return {"message": "Product deleted"}

    return False
