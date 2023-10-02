from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    func,
)

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
