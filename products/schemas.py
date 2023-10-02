import datetime

from pydantic import BaseModel


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


class CreateProduct(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode: True


class DeleteProduct(BaseModel):
    message: str
