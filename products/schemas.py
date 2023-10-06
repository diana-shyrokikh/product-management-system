import datetime

from pydantic import (
    BaseModel,
    field_validator
)

from validators import (
    validate_string,
    validate_number
)


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
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
    quantity: int
    category_id: int

    @field_validator("name")
    def validate_name(cls, name):
        return validate_string(
            name,
            r"^[A-Za-z][A-Za-z0-9\s]*$",
            "Name must only contain letters, "
            "numbers, or spaces and start with letter"
        )

    @field_validator("description")
    def validate_description(cls, description):
        return validate_string(
            description,
            r"^[A-Za-z][A-Za-z0-9\s]*$",
            "Description must only contain letters, "
            "numbers, or spaces and start with letter"
        )

    @field_validator("price")
    def validate_price(cls, price):
        return validate_number(
            price, "Price"
        )

    @field_validator("quantity")
    def validate_quantity(cls, quantity):
        return validate_number(
            quantity, "Count"
        )

    @field_validator("category_id")
    def validate_category_id(cls, category_id):
        return validate_number(
            category_id, "Category id"
        )


class UpdateProduct(CreateProduct):
    name: str = None
    description: str = None
    price: float = None
    quantity: int = None
    category_id: int = None


class Product(ProductBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode: True


class DeleteProduct(BaseModel):
    message: str


class OrderProduct(BaseModel):
    id: int
    quantity: int = 1


class BuyProduct(BaseModel):
    id: int
    name: str
    price: float
    quantity: int = 1
