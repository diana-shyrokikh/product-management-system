from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum

from database import Base


class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id = Column(ForeignKey("orders.id"), primary_key=True)
    product_id = Column(ForeignKey("products.id"), primary_key=True)
    product_quantity = Column(Integer, default=1)
    order = relationship("Order", back_populates="products")
    product = relationship("Product", back_populates="orders")


class StatusEnum(str, Enum):
    paid = "Paid"
    pending = "Pending"


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer, primary_key=True, index=True
    )
    status = Column(
        SQLAlchemyEnum(StatusEnum)
    )
    created_at = Column(
        DateTime, server_default=func.now()
    )
    total_price = Column(Integer, default=1)
    user_id = Column(
        Integer, ForeignKey(
            "users.id", ondelete="CASCADE"
        )
    )

    user = relationship(
        "User", back_populates="orders"
    )
    products = relationship(
        "OrderProduct", back_populates="order"
    )
