from fastapi import status

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from orders.models import order_products
from orders.stripe_helper import create_stripe_session
from products import crud as products_crud

from orders import models, schemas


async def create_order(
    db: AsyncSession,
    order: schemas.CreateOrder,
    user_id: int,
    username: str
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

    payment_url = create_stripe_session(
        username=username,
        order_id=order_index,
        total_price=total_price
    )

    new_order = {
        "products": products,
        "id": order_index,
        "status": "pending",
        "total_price": total_price,
        "payment_url": payment_url
    }

    return new_order


async def update_order(
        db: AsyncSession,
        updated_order: models.Order,
) -> models.Order:
    updated_order.status = "paid"

    await db.commit()
    await db.refresh(updated_order)

    return updated_order


async def delete_order(
        db: AsyncSession,
        deleted_order: models.Order,
) -> True:
    await db.delete(deleted_order)
    await db.commit()

    return True


async def update_or_delete_order(
        db: AsyncSession,
        order_id: int,
        order_status: str,
        user_id: int = None,
        username: str = None,
) -> [models.Order | None]:
    query = select(models.Order).where(
        models.Order.id == order_id
    )

    order = await db.execute(query)
    order = order.fetchone()

    if order:
        order = order[0]

    if order_status == "paid":
        await update_order(db, order)
        return {"message": "Payment successful"}
    else:
        await delete_order(db, order)
        return {
            "message":
                "Payment canceled, the order was deleted"
        }
