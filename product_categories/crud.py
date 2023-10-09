from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from product_categories import models, schemas


async def get_all_categories(
        db: AsyncSession,
) -> list[models.ProductCategory]:
    query = select(models.ProductCategory)
    category_list = await db.execute(query)
    return [
        category[0]
        for category
        in category_list.fetchall()
    ]


async def get_category(
        db: AsyncSession,
        category_id: int
) -> [models.ProductCategory | None]:
    query = select(models.ProductCategory).where(
        models.ProductCategory.id == category_id
    )
    category = await db.execute(query)
    category = category.fetchone()

    if category:
        return category[0]

    return None


async def get_category_by_name(
        db: AsyncSession,
        category_name: str
) -> [models.ProductCategory | None]:
    query = select(models.ProductCategory).where(
        models.ProductCategory.name == category_name
    )
    category = await db.execute(query)
    category = category.fetchone()

    if category:
        return category[0]

    return None


async def create_category(
        db: AsyncSession,
        category: schemas.CreateCategory
) -> dict:
    category.name = category.name.strip().capitalize()

    query = insert(models.ProductCategory).values(
        name=category.name,
    )

    new_category = await db.execute(query)

    await db.commit()

    new_category = {
        **category.model_dump(),
        "id": new_category.lastrowid,
    }

    return new_category


async def update_category(
        db: AsyncSession,
        category_id: int,
        new_data: schemas.UpdateCategory,
) -> [models.ProductCategory | None]:
    query = select(models.ProductCategory).where(
        models.ProductCategory.id == category_id
    )
    updated_category = await db.execute(query)
    updated_category = updated_category.fetchone()

    if updated_category:
        updated_category = updated_category[0]

        if new_data.name:
            updated_category.name = new_data.name.strip().capitalize()

        await db.commit()
        await db.refresh(updated_category)

        return updated_category

    return None


async def delete_category(
        db: AsyncSession,
        category_id: int,
) -> [dict | bool]:
    query = select(models.ProductCategory).where(
        models.ProductCategory.id == category_id
    )
    deleted_category = await db.execute(query)
    deleted_category = deleted_category.fetchone()

    if deleted_category:
        await db.delete(deleted_category[0])
        await db.commit()

        return {"message": "Category deleted"}

    return False
