import datetime
import re

from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

    class Config:
        json_encoders = {
            datetime.datetime: lambda dt: dt.strftime(
                "%Y-%m-%dT%H:%M"
            )
        }


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

    @field_validator("name")
    def validate_name(cls, name):
        pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

        if not re.match(pattern, name):
            raise ValueError(
                "Name must only contain letters, "
                "numbers, or spaces"
            )

        return name

    @field_validator("description")
    def validate_description(cls, description):
        pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

        if not re.match(pattern, description):
            raise ValueError(
                "Description must only contain letters, "
                "numbers, or spaces"
            )

        return description

    @field_validator("price")
    def validate_price(cls, price):
        if float(price) < 1:
            raise ValueError("Price must be greater than 0")

        return price

    @field_validator("category_id")
    def validate_category_id(cls, category_id):
        if float(category_id) < 1:
            raise ValueError("Category id must be greater than 0")

        return category_id


class UpdateProduct(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    category_id: int = None

    @field_validator("name")
    def validate_name(cls, name):
        if name:
            pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

            if not re.match(pattern, name):
                raise ValueError(
                    "Name must only contain letters, "
                    "numbers, or spaces"
                )

            return name

    @field_validator("description")
    def validate_description(cls, description):
        if description:
            pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

            if not re.match(pattern, description):
                raise ValueError(
                    "Description must only contain letters, "
                    "numbers, or spaces"
                )

            return description

    @field_validator("price")
    def validate_price(cls, price):
        if price:
            if float(price) < 1:
                raise ValueError("Price must be greater than 0")

            return price

    @field_validator("category_id")
    def validate_category_id(cls, category_id):
        if category_id:
            if float(category_id) < 1:
                raise ValueError("Category id must be greater than 0")

            return category_id


class Product(ProductBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode: True


class DeleteProduct(BaseModel):
    message: str
