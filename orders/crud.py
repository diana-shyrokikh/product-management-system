from fastapi import status

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from orders.stripe_helper import create_stripe_session
from products import crud as products_crud

from orders import models, schemas
from users.email_notification_helper import send_email


async def get_all_orders(
    db: AsyncSession,
) -> list[dict]:
    query = select(models.Order).options(
        selectinload(
            models.Order.products
        ).joinedload(models.OrderProduct.product)
    )

    orders = await db.execute(query)

    orders_list = []
    for order in orders.scalars().all():
        products = []
        for ordered_product in order.products:
            products.append({
                "id": ordered_product.product.id,
                "name": ordered_product.product.name,
                "price": float(ordered_product.product.price),
                "quantity": ordered_product.product_quantity
            })

        orders_list.append({
            "id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "products": products
        })

    return orders_list


async def get_order(
    db: AsyncSession,
    order_id: int,
) -> [dict | None]:
    query = (select(models.Order).where(
        models.Order.id == order_id
    ).options(
        selectinload(
            models.Order.products
        ).joinedload(models.OrderProduct.product)
    ))

    order = await db.execute(query)
    order = order.scalar_one_or_none()

    if order:
        products = []

        for ordered_product in order.products:
            products.append({
                "id": ordered_product.product.id,
                "name": ordered_product.product.name,
                "price": float(ordered_product.product.price),
                "quantity": ordered_product.product_quantity
            })

        order = {
            "id": order.id,
            "total_price": float(order.total_price),
            "status": order.status.value,
            "products": products
        }

        return order

    return None


async def create_order(
    db: AsyncSession,
    order: schemas.CreateOrder,
    user_id: int,
    username: str,
    user_email: str,
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
        order_product = insert(models.OrderProduct).values(
            order_id=order_index,
            product_id=product.id,
            product_quantity=product.quantity
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

    send_email(new_order, user_email)

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
        order_status: str
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
