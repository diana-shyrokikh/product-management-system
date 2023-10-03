import datetime
import re

from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    description: str
    price: float

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


class UpdateProduct(BaseModel):
    name: str = None
    description: str = None
    price: float = None

    @field_validator("name")
    def validate_name(cls, name):
        if name is not None:
            pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

            if not re.match(pattern, name):
                raise ValueError(
                    "Name must only contain letters, "
                    "numbers, or spaces"
                )

            return name

    @field_validator("description")
    def validate_description(cls, description):
        if description is not None:
            pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

            if not re.match(pattern, description):
                raise ValueError(
                    "Description must only contain letters, "
                    "numbers, or spaces"
                )

            return description

    @field_validator("price")
    def validate_price(cls, price):
        if price is not None:
            if float(price) < 1:
                raise ValueError("Price must be greater than 0")
            return price


class Product(ProductBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode: True


class DeleteProduct(BaseModel):
    message: str
