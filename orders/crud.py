from fastapi import status

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from orders.models import order_products
from products import crud as products_crud

from orders import models, schemas


async def create_order(
    db: AsyncSession,
    order: schemas.CreateOrder,
    user_id: int
) -> [dict | None]:
    total_price = 0
    products = []

    for product in order.products:
        db_product = await products_crud.get_product(
            db=db,
            product_id=product.id
        )
        if not db_product:
            return status.HTTP_404_NOT_FOUND

        if db_product.quantity < product.quantity:
            return status.HTTP_406_NOT_ACCEPTABLE

        total_price += float(
            product.quantity * db_product.price
        )

        products.append({
            "id": product.id,
            "name": db_product.name,
            "price": db_product.price,
            "quantity": product.quantity
        })

        db_product.quantity -= product.quantity

        await db.commit()
        await db.refresh(db_product)

    query = insert(models.Order).values(
        status="pending",
        total_price=total_price,
        user_id=user_id,
    )
    new_order = await db.execute(query)

    order_index = new_order.lastrowid
    for product in order.products:
        order_product = insert(order_products).values(
            order_id=order_index,
            product_id=product.id,
        )
        await db.execute(order_product)

    await db.commit()

    new_order = {
        "products": products,
        "id": order_index,
        "status": "pending",
        "total_price": total_price,
    }

    return new_order
