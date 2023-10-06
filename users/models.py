from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, index=True
    )
    username = Column(
        String(255), unique=True, nullable=False
    )
    email = Column(
        String(255), unique=True, nullable=False
    )
    phone_number = Column(
        String(255), unique=True, nullable=False
    )
    password = Column(
        String(255), nullable=False
    )
    is_admin = Column(
        Boolean(), default=False
    )
    is_activated = Column(
        Boolean(), default=False
    )

    orders = relationship(
        "Order", back_populates="user"
    )
