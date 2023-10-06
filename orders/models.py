from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func,
    ForeignKey,
    Table,
)

from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum

from database import Base


order_products = Table(
    "order_products",
    Base.metadata,
    Column(
        "order_id",
        Integer,
        ForeignKey("orders.id"),
        primary_key=True
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id"),
        primary_key=True
    ),
)


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
        "Product",
        secondary=order_products,
        back_populates="orders"
    )
