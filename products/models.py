from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship

import product_categories.models
from orders.models import order_products

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer, primary_key=True, index=True
    )
    name = Column(
        String(255), unique=True, nullable=False
    )
    description = Column(
        String(512), nullable=False
    )
    price = Column(
        Numeric(precision=10, scale=2), nullable=False
    )
    created_at = Column(
        DateTime, server_default=func.now()
    )
    quantity = Column(Integer, default=0)
    category_id = Column(
        Integer, ForeignKey(
            "product_categories.id", ondelete="CASCADE"
        )
    )

    category = relationship(
        product_categories.models.ProductCategory
    )
    orders = relationship(
        "OrderProduct", back_populates="product"
    )
