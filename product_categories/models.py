from sqlalchemy import (
    Column,
    Integer,
    String,
)

from database import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(
        Integer, primary_key=True, index=True
    )
    name = Column(
        String(255), unique=True, nullable=False
    )
